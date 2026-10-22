// Shared helpers for the member API. No packages needed: Node's own crypto + fetch.
// Environment variables (set in Vercel):
//   STRIPE_SECRET_KEY  - restricted key with read access to Checkout Sessions, Customers, Subscriptions
//   MEMBER_SECRET      - any long random string, used to sign member passes
//   MEMBER_BOOK_URL    - the $50 member booking page
//   LIBRARY_JSON       - optional; JSON list of classes [{title, length, url, topic}]
const crypto = require("crypto");

const DAY = 86400000;

function sign(payload) {
  const body = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const mac = crypto.createHmac("sha256", process.env.MEMBER_SECRET || "dev-secret").update(body).digest("base64url");
  return `${body}.${mac}`;
}

function verify(pass) {
  if (!pass || !pass.includes(".")) return null;
  const [body, mac] = pass.split(".");
  const good = crypto.createHmac("sha256", process.env.MEMBER_SECRET || "dev-secret").update(body).digest("base64url");
  if (mac.length !== good.length || !crypto.timingSafeEqual(Buffer.from(mac), Buffer.from(good))) return null;
  const data = JSON.parse(Buffer.from(body, "base64url").toString());
  return data.exp > Date.now() ? data : null;
}

// Backup unlock while there's no Stripe key: one member code, derived from MEMBER_SECRET.
// It goes in the Stripe payment links' after-payment address, so only payers see it.
function joinCode() {
  return crypto.createHmac("sha256", process.env.MEMBER_SECRET || "dev-secret").update("nest-join").digest("hex").slice(0, 12);
}
const hasStripe = () => !!process.env.STRIPE_SECRET_KEY;

async function stripe(path) {
  const r = await fetch(`https://api.stripe.com/v1/${path}`, {
    headers: { Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}` },
  });
  if (!r.ok) throw new Error(`Stripe ${r.status}`);
  return r.json();
}

// Is there an active (or trialing) subscription for this email?
async function activeMember(email) {
  const customers = await stripe(`customers?limit=10&email=${encodeURIComponent(email)}`);
  for (const c of customers.data) {
    const subs = await stripe(`subscriptions?customer=${c.id}&status=all&limit=10`);
    const live = subs.data.find((s) => ["active", "trialing", "past_due"].includes(s.status));
    if (live) return { email, until: live.current_period_end * 1000 || Date.now() + 31 * DAY };
  }
  return null;
}

// A pass lasts until the paid period ends, plus a few days of grace, max 40 days.
function passFor(member, maxDays = 40) {
  const exp = Math.min(member.until + 3 * DAY, Date.now() + maxDays * DAY);
  return { pass: sign({ email: member.email, exp }), exp };
}

function send(res, status, data) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(data));
}

async function readJSON(req) {
  if (req.body && typeof req.body === "object") return req.body;
  let raw = "";
  for await (const chunk of req) raw += chunk;
  try { return JSON.parse(raw || "{}"); } catch { return {}; }
}

module.exports = { sign, verify, stripe, activeMember, passFor, send, readJSON, joinCode, hasStripe };

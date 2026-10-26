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

// Free Nest time that comes with a purchase: Stripe payment link id -> days of Nest, and where to book.
// A $75 support call includes 1 month; the $444 Human Design reading includes 3 months.
const GUEST = {
  plink_1UTTxQDcPgQXcI4deYUSfxF0: { days: 31, book: "https://calendar.app.google/gczW5R1ubjrYmJo7A", what: "call" },
  plink_1UUwycDcPgQXcI4dMCTXpWJZ: { days: 92, book: "https://calendar.app.google/K7LF7T2FPzPinaS48", what: "reading" },
};

// Completed guest purchases still inside their free window: [{ email, until }]
async function guestGrants() {
  const out = [];
  for (const [link, g] of Object.entries(GUEST)) {
    const since = Math.floor(Date.now() / 1000) - g.days * 86400;
    let after = "";
    for (let page = 0; page < 10; page++) {
      const r = await stripe(`checkout/sessions?payment_link=${link}&status=complete&limit=100&created[gte]=${since}${after}`);
      for (const x of r.data) {
        const email = x.customer_details && x.customer_details.email;
        if (email) out.push({ email: email.toLowerCase(), until: (x.created + g.days * 86400) * 1000 });
      }
      if (!r.has_more) break;
      after = `&starting_after=${r.data[r.data.length - 1].id}`;
    }
  }
  return out;
}

// Is there an active (or trialing) subscription for this email? If not, free Nest time from a call or reading?
async function activeMember(email) {
  const customers = await stripe(`customers?limit=10&email=${encodeURIComponent(email)}`);
  for (const c of customers.data) {
    const subs = await stripe(`subscriptions?customer=${c.id}&status=all&limit=10`);
    const live = subs.data.find((s) => ["active", "trialing", "past_due"].includes(s.status));
    if (live) return { email, until: live.current_period_end * 1000 || Date.now() + 31 * DAY };
  }
  const mine = (await guestGrants()).filter((g) => g.email === email.toLowerCase()).sort((a, b) => b.until - a.until)[0];
  if (mine && mine.until > Date.now()) return { email, until: mine.until, guest: true };
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

// Mailchimp: mark someone as a Nest member (or not) on The Emotional Support Line list.
// New contacts are added as "transactional" (they bought; they didn't ask for marketing email).
const MC_LIST = "bd683fce4d", NEST_TAG = "Nest member";
function mc() {
  const key = process.env.MAILCHIMP_API_KEY || "", dc = key.split("-")[1];
  if (!key || !dc) return null;
  return { base: `https://${dc}.api.mailchimp.com/3.0/lists/${MC_LIST}`, headers: { Authorization: "Basic " + Buffer.from("esl:" + key).toString("base64"), "Content-Type": "application/json" } };
}
async function nestTag(email, active) {
  const m = mc();
  if (!m || !email || !email.includes("@")) return;
  const hash = crypto.createHash("md5").update(email.toLowerCase()).digest("hex");
  if (active) await fetch(`${m.base}/members/${hash}`, { method: "PUT", headers: m.headers, body: JSON.stringify({ email_address: email.toLowerCase(), status_if_new: "transactional" }) });
  await fetch(`${m.base}/members/${hash}/tags`, { method: "POST", headers: m.headers, body: JSON.stringify({ tags: [{ name: NEST_TAG, status: active ? "active" : "inactive" }] }) });
}

module.exports = { GUEST, guestGrants, mc, nestTag, NEST_TAG, sign, verify, stripe, activeMember, passFor, send, readJSON, joinCode, hasStripe };

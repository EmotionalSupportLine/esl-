// Energy Forecast / waiting-list sign-up straight through the Mailchimp API, so visitors never
// see Mailchimp's "Confirm Humanity" page. New people still get Mailchimp's confirmation email
// (double opt-in: status "pending"). Existing subscribers just get their answers updated.
// Needs MAILCHIMP_API_KEY in Vercel. Without it, answers {fallback:true} and the page uses
// Mailchimp's own form instead.
const crypto = require("crypto");
const { send, readJSON } = require("./_lib");
const LIST = "bd683fce4d";
const WAITLIST_TAG = "Support Plan waiting list";

module.exports = async (req, res) => {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST." });
  const key = process.env.MAILCHIMP_API_KEY || "";
  const dc = key.split("-")[1];
  if (!key || !dc) return send(res, 200, { fallback: true });
  try {
    const b = await readJSON(req);
    if (b.hp) return send(res, 200, { status: "pending" }); // honeypot: bots fill hidden fields
    const email = String(b.email || "").trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || email.length > 200) return send(res, 400, { error: "Please check the email address." });
    const merge = {};
    if (b.fname) merge.FNAME = String(b.fname).slice(0, 60);
    if (b.spprice) merge.SPPRICE = String(b.spprice).slice(0, 20);
    const hash = crypto.createHash("md5").update(email).digest("hex");
    const base = `https://${dc}.api.mailchimp.com/3.0/lists/${LIST}/members/${hash}`;
    const auth = { Authorization: "Basic " + Buffer.from("esl:" + key).toString("base64"), "Content-Type": "application/json" };
    const r = await fetch(base, { method: "PUT", headers: auth, body: JSON.stringify({ email_address: email, status_if_new: "pending", merge_fields: merge }) });
    const m = await r.json().catch(() => ({}));
    if (!r.ok || m.status === "unsubscribed") return send(res, 200, { fallback: true }); // e.g. someone who left before: Mailchimp's own form lets them rejoin
    if (b.spprice) {
      await fetch(base + "/tags", { method: "POST", headers: auth, body: JSON.stringify({ tags: [{ name: WAITLIST_TAG, status: "active" }] }) }).catch(() => {});
    }
    send(res, 200, { status: m.status === "subscribed" ? "subscribed" : "pending" });
  } catch (e) {
    send(res, 200, { fallback: true });
  }
};

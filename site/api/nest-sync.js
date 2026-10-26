// Daily (Vercel cron): keep two Mailchimp tags matching Stripe.
// "Nest member": everyone with an active, trialing or past-due subscription, or free Nest time from a
//   support call (1 month) or Human Design reading (3 months). Removed when that ends.
// "Nest ending soon": free-time guests (not paying members) whose time ends within 5 days. A Mailchimp
//   automation sends the "Your free time in the Nest ends in a few days" email when this tag is added.
//   Removed once their time ends or they join, so a later purchase can trigger it again.
// Needs STRIPE_SECRET_KEY and MAILCHIMP_API_KEY. Safe to run by hand: it only adds or removes these tags.
const crypto = require("crypto");
const { stripe, send, hasStripe, mc, nestTag, NEST_TAG, guestGrants } = require("./_lib");
const ENDING_TAG = "Nest ending soon";
const DAY = 86400000;

module.exports = async (req, res) => {
  const m = mc();
  if (!hasStripe() || !m) return send(res, 200, { skipped: "Needs STRIPE_SECRET_KEY and MAILCHIMP_API_KEY." });
  try {
    // Paying members
    const paying = new Set();
    for (const status of ["active", "trialing", "past_due"]) {
      let after = "";
      for (let page = 0; page < 20; page++) {
        const r = await stripe(`subscriptions?status=${status}&limit=100&expand[]=data.customer${after}`);
        for (const s of r.data) if (s.customer && s.customer.email) paying.add(s.customer.email.toLowerCase());
        if (!r.has_more) break;
        after = `&starting_after=${r.data[r.data.length - 1].id}`;
      }
    }
    // Free-time guests: latest end date per email
    const guestUntil = new Map();
    for (const g of await guestGrants()) if (g.until > Date.now() && (guestUntil.get(g.email) || 0) < g.until) guestUntil.set(g.email, g.until);

    const members = new Set([...paying, ...guestUntil.keys()]);
    const ending = new Set([...guestUntil].filter(([e, u]) => !paying.has(e) && u - Date.now() <= 5 * DAY).map(([e]) => e));

    const segs = await (await fetch(`${m.base}/segments?type=static&count=1000`, { headers: m.headers })).json();
    async function tagged(name) {
      const seg = (segs.segments || []).find((s) => s.name === name);
      const out = new Set();
      if (!seg) return out;
      for (let offset = 0; offset < 10000; offset += 1000) {
        const r = await (await fetch(`${m.base}/segments/${seg.id}/members?count=1000&offset=${offset}`, { headers: m.headers })).json();
        for (const x of r.members || []) out.add(x.email_address.toLowerCase());
        if (!r.members || r.members.length < 1000) break;
      }
      return out;
    }
    async function setTag(email, name, active) {
      const hash = crypto.createHash("md5").update(email).digest("hex");
      await fetch(`${m.base}/members/${hash}/tags`, { method: "POST", headers: m.headers, body: JSON.stringify({ tags: [{ name, status: active ? "active" : "inactive" }] }) });
    }

    const result = { members: members.size, added: 0, removed: 0, endingSoon: ending.size, endingTagged: 0, endingCleared: 0 };
    const hasMember = await tagged(NEST_TAG);
    for (const e of members) if (!hasMember.has(e)) { await nestTag(e, true).catch(() => {}); result.added++; }
    for (const e of hasMember) if (!members.has(e)) { await nestTag(e, false).catch(() => {}); result.removed++; }

    const hasEnding = await tagged(ENDING_TAG);
    for (const e of ending) if (!hasEnding.has(e)) { await setTag(e, ENDING_TAG, true).catch(() => {}); result.endingTagged++; }
    for (const e of hasEnding) if (!ending.has(e)) { await setTag(e, ENDING_TAG, false).catch(() => {}); result.endingCleared++; }

    send(res, 200, result);
  } catch (e) {
    send(res, 500, { error: "Sync failed: " + e.message });
  }
};

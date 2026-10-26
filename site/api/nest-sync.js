// Daily (Vercel cron): keep the Mailchimp tag "Nest member" matching Stripe.
// Everyone with an active, trialing or past-due subscription, or free Nest time from a call or reading, gets the tag;
// anyone who cancelled or whose free time ran out loses it.
// Needs STRIPE_SECRET_KEY and MAILCHIMP_API_KEY. Safe to run by hand: it only adds or removes that one tag.
const { stripe, send, hasStripe, mc, nestTag, NEST_TAG, guestGrants } = require("./_lib");

module.exports = async (req, res) => {
  const m = mc();
  if (!hasStripe() || !m) return send(res, 200, { skipped: "Needs STRIPE_SECRET_KEY and MAILCHIMP_API_KEY." });
  try {
    const members = new Set();
    for (const status of ["active", "trialing", "past_due"]) {
      let after = "";
      for (let page = 0; page < 20; page++) {
        const r = await stripe(`subscriptions?status=${status}&limit=100&expand[]=data.customer${after}`);
        for (const s of r.data) if (s.customer && s.customer.email) members.add(s.customer.email.toLowerCase());
        if (!r.has_more) break;
        after = `&starting_after=${r.data[r.data.length - 1].id}`;
      }
    }
    // Free Nest time from a support call (1 month) or Human Design reading (3 months)
    for (const g of await guestGrants()) members.add(g.email);
    // Who has the tag now?
    const segs = await (await fetch(`${m.base}/segments?type=static&count=1000`, { headers: m.headers })).json();
    const seg = (segs.segments || []).find((s) => s.name === NEST_TAG);
    const tagged = new Set();
    if (seg) {
      for (let offset = 0; offset < 10000; offset += 1000) {
        const r = await (await fetch(`${m.base}/segments/${seg.id}/members?count=1000&offset=${offset}`, { headers: m.headers })).json();
        for (const x of r.members || []) tagged.add(x.email_address.toLowerCase());
        if (!r.members || r.members.length < 1000) break;
      }
    }
    let added = 0, removed = 0;
    for (const e of members) if (!tagged.has(e)) { await nestTag(e, true).catch(() => {}); added++; }
    for (const e of tagged) if (!members.has(e)) { await nestTag(e, false).catch(() => {}); removed++; }
    send(res, 200, { members: members.size, added, removed });
  } catch (e) {
    send(res, 500, { error: "Sync failed: " + e.message });
  }
};

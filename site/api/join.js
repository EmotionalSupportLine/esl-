// After Stripe checkout: /app/?session_id=cs_...&k=CODE calls this to turn the purchase into a member pass.
const { stripe, activeMember, passFor, send, joinCode, hasStripe, nestTag } = require("./_lib");
const DAY = 86400000;

module.exports = async (req, res) => {
  try {
    const q = new URL(req.url, "http://x").searchParams;
    const id = q.get("session_id"), k = q.get("k");
    if (hasStripe() && id && id.startsWith("cs_")) {
      const s = await stripe(`checkout/sessions/${id}`);
      const email = s.customer_details && s.customer_details.email;
      if (s.status !== "complete" || !email) return send(res, 402, { error: "This checkout isn't finished yet." });
      const member = (await activeMember(email)) || { email, until: Date.now() + 31 * DAY };
      await nestTag(email, true).catch(() => {}); // Mailchimp: tag "Nest member"
      return send(res, 200, { email, code: joinCode(), ...passFor(member) });
    }
    if (k && k === joinCode()) {
      return send(res, 200, { email: "member", code: k, ...passFor({ email: "member", until: Date.now() + 400 * DAY }, 403) });
    }
    send(res, 400, { error: "That link didn't unlock the Nest. Use Restore access with your member code." });
  } catch (e) {
    send(res, 500, { error: "Couldn't confirm your membership. Try again in a minute." });
  }
};

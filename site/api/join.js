// After Stripe checkout: /app/?session_id=cs_... calls this to turn the purchase into a member pass.
const { stripe, activeMember, passFor, send } = require("./_lib");

module.exports = async (req, res) => {
  try {
    const id = new URL(req.url, "http://x").searchParams.get("session_id");
    if (!id || !id.startsWith("cs_")) return send(res, 400, { error: "Missing checkout session." });
    const s = await stripe(`checkout/sessions/${id}`);
    const email = s.customer_details && s.customer_details.email;
    if (s.status !== "complete" || !email) return send(res, 402, { error: "This checkout isn't finished yet." });
    const member = (await activeMember(email)) || { email, until: Date.now() + 31 * 86400000 };
    send(res, 200, { email, ...passFor(member) });
  } catch (e) {
    send(res, 500, { error: "Couldn't confirm your membership. Try again in a minute." });
  }
};

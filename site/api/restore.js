// New phone or cleared browser: member enters their email (checked with Stripe) or member code.
const { activeMember, passFor, send, readJSON, joinCode, hasStripe } = require("./_lib");

module.exports = async (req, res) => {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST." });
  try {
    const { email, code } = await readJSON(req);
    const c = (code || email || "").trim().toLowerCase();
    if (c && c === joinCode()) return send(res, 200, { email: "member", code: c, ...passFor({ email: "member", until: Date.now() + 400 * 86400000 }, 403) });
    if (!hasStripe()) return send(res, 404, { error: "That code didn't match. Check your welcome email, or write to careteam@theemotionalsupportline.com." });
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return send(res, 400, { error: "Enter the email you used at checkout, or your member code." });
    const member = await activeMember(email.trim().toLowerCase());
    if (!member) return send(res, 404, { error: "No active membership for that email. Check for typos, or join below." });
    send(res, 200, { email: member.email, code: joinCode(), ...passFor(member) });
  } catch (e) {
    send(res, 500, { error: "Couldn't check membership right now. Try again in a minute." });
  }
};

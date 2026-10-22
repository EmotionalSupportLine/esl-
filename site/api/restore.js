// New phone or cleared browser: member types the email they paid with.
const { activeMember, passFor, send, readJSON } = require("./_lib");

module.exports = async (req, res) => {
  if (req.method !== "POST") return send(res, 405, { error: "Use POST." });
  try {
    const { email } = await readJSON(req);
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return send(res, 400, { error: "Enter the email you used at checkout." });
    const member = await activeMember(email.trim().toLowerCase());
    if (!member) return send(res, 404, { error: "No active membership for that email. Check for typos, or join below." });
    send(res, 200, { email: member.email, ...passFor(member) });
  } catch (e) {
    send(res, 500, { error: "Couldn't check membership right now. Try again in a minute." });
  }
};

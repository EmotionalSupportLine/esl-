// Member-only content: the class library and the $50 booking link.
// Kept on the server so the links aren't sitting in public page code.
const { verify, send } = require("./_lib");
const fallbackLibrary = require("./_library.json");

module.exports = async (req, res) => {
  const pass = (req.headers.authorization || "").replace(/^Bearer /, "");
  const member = verify(pass);
  if (!member) return send(res, 401, { error: "Your pass has expired. Restore access with your email." });
  let library = fallbackLibrary;
  try { if (process.env.LIBRARY_JSON) library = JSON.parse(process.env.LIBRARY_JSON); } catch {}
  send(res, 200, {
    email: member.email,
    exp: member.exp,
    memberBookUrl: process.env.MEMBER_BOOK_URL || "",
    groupCall: process.env.GROUP_CALL || "First Tuesday of the month, 6 pm Mountain. The link arrives by email.",
    library,
  });
};

// Neutrino widget -> Mailchimp. Neutrino's "Webhook" integration posts every chart made in the
// widget (name, email, marketing consent and the full chart) to this address. We keep only the
// email, first name and consent, and drop everything else: no birth data is stored here or sent on.
//   - agreed to marketing emails -> subscribed to the Energy Forecast audience, tag "Neutrino widget"
//   - did not agree               -> kept as a "transactional" contact (no marketing), same tag
// Existing subscribers are never downgraded. The URL carries ?k=<NEUTRINO_HOOK_SECRET> (Vercel).
const crypto = require("crypto");
const { send, readJSON } = require("./_lib");
const LIST = "bd683fce4d";
const TAG = "Neutrino widget";

// Walk the payload and collect [path, value] pairs, so we work whatever Neutrino names its fields.
function walk(o, path = "", out = []) {
  if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) walk(v, path ? `${path}.${k}` : k, out);
  else out.push([path, o]);
  return out;
}

module.exports = async (req, res) => {
  const secret = process.env.NEUTRINO_HOOK_SECRET || "";
  const k = new URL(req.url, "http://x").searchParams.get("k") || "";
  if (!secret || k.length !== secret.length || !crypto.timingSafeEqual(Buffer.from(k), Buffer.from(secret))) return send(res, 401, { error: "Not allowed." });
  const key = process.env.MAILCHIMP_API_KEY || "";
  const dc = key.split("-")[1];
  // Owner check (needs the secret): GET ?k=...&check=email shows that contact's Mailchimp status and tags.
  const check = new URL(req.url, "http://x").searchParams.get("check");
  if (req.method === "GET" && check && dc) {
    const h = crypto.createHash("md5").update(check.trim().toLowerCase()).digest("hex");
    const m = await (await fetch(`https://${dc}.api.mailchimp.com/3.0/lists/${LIST}/members/${h}`, { headers: { Authorization: "Basic " + Buffer.from("esl:" + key).toString("base64") } })).json().catch(() => ({}));
    return send(res, 200, { status: m.status, tags: (m.tags || []).map((t) => t.name), last_changed: m.last_changed });
  }
  if (req.method !== "POST") return send(res, 405, { error: "Use POST." });
  try {
    const flat = walk(await readJSON(req));
    console.log("neutrino-hook fields:", flat.map(([p]) => p).filter((p) => !/chart|gate|planet|center|channel|birth|design|personality/i.test(p)).slice(0, 40).join(", "));
    const email = String((flat.find(([p, v]) => /e-?mail/i.test(p) && /@/.test(String(v))) || [])[1] || "").trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || email.length > 200) return send(res, 200, { ok: true, skipped: "no email" });
    const nameRaw = String((flat.find(([p, v]) => /(^|\.)(first_?name|firstName|name)$/i.test(p) && typeof v === "string" && v && !/@/.test(v)) || [])[1] || "");
    const fname = nameRaw.trim().split(/\s+/)[0].slice(0, 60);
    const consent = flat.some(([p, v]) => /consent|marketing|opt_?in|optIn|newsletter|subscribe/i.test(p) && (v === true || v === "true" || v === 1 || v === "yes"));
    if (!key || !dc) return send(res, 200, { ok: true, skipped: "no Mailchimp key" });
    const hash = crypto.createHash("md5").update(email).digest("hex");
    const base = `https://${dc}.api.mailchimp.com/3.0/lists/${LIST}/members/${hash}`;
    const auth = { Authorization: "Basic " + Buffer.from("esl:" + key).toString("base64"), "Content-Type": "application/json" };
    const now = await (await fetch(base, { headers: auth })).json().catch(() => ({}));
    const body = { email_address: email, merge_fields: fname ? { FNAME: fname } : {} };
    if (!now.status || now.status === 404) body.status = consent ? "subscribed" : "transactional";
    else if (consent && now.status === "transactional") body.status = "subscribed"; // they've now said yes
    // "unsubscribed" or "cleaned" stay as they are: we never resubscribe someone who left.
    const r = await fetch(base, { method: "PUT", headers: auth, body: JSON.stringify({ ...body, status_if_new: body.status || (consent ? "subscribed" : "transactional") }) });
    if (r.ok) await fetch(base + "/tags", { method: "POST", headers: auth, body: JSON.stringify({ tags: [{ name: TAG, status: "active" }, ...(consent ? [{ name: "Neutrino opt-in", status: "active" }] : [])] }) }).catch(() => {});
    send(res, 200, { ok: r.ok, consent });
  } catch (e) {
    console.log("neutrino-hook error:", e.message);
    send(res, 200, { ok: false });
  }
};

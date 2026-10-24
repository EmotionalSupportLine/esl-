// Crisis safety pop-up. Included on every page.
// If anything typed into the site mentions suicide, self-harm, harming someone or a mental
// health emergency, show a calm message pointing to 988 and 911. Nothing typed is stored or sent.
(function () {
  var PATTERNS = [
    /suicid/i, /kill (my ?self|me)\b/i, /end (it all|my life|things)\b/i, /(want|wanna|going) to die\b/i, /wish i (was|were) dead/i,
    /(don'?t|do not) want to (live|be alive|be here|wake up)/i, /better off (dead|without me)/i, /no reason to live/i,
    /self[- ]?harm/i, /(cut|cutting|hurt|hurting|harm|harming) (my ?self|myself)/i, /overdos/i, /take all (my|the) pills/i,
    /(kill|hurt|harm|shoot|stab) (him|her|them|someone|somebody|my (husband|wife|partner|kid|child|son|daughter|mom|dad|boss))\b/i,
    /homicid/i, /hearing voices/i, /psychos/i, /losing touch with reality/i, /\b(si|hi)\b ?(thoughts|ideation)/i, /(suicidal|homicidal) ideation/i, /i('m| am) not safe/i,
    /(mental health|psychiatric) (crisis|emergency)/i, /in danger\b/i, /(he|she|they)('s| is| are) (hurting|hitting|going to hurt) me/i
  ];
  var shown = false;

  function style() {
    var css = ".cg-back{position:fixed;inset:0;background:rgba(13,58,61,.72);display:flex;align-items:center;justify-content:center;padding:16px;z-index:9999}" +
      ".cg-box{background:#fff8ec;color:#1f1c1c;border-radius:22px;max-width:460px;width:100%;padding:28px 26px 22px;box-shadow:0 30px 60px -20px rgba(0,0,0,.5);font:400 17px/1.55 Nunito,system-ui,sans-serif}" +
      ".cg-box h2{font:700 1.5rem/1.2 Lora,Georgia,serif;margin:0 0 10px;color:#134f53}" +
      ".cg-box p{margin:0 0 14px}.cg-btns{display:grid;gap:10px;margin:18px 0 12px}" +
      ".cg-btns a{display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:999px;font:800 1.05rem Nunito,system-ui,sans-serif;text-decoration:none}" +
      ".cg-988{background:#d7783a;color:#fff}.cg-txt{background:#134f53;color:#fcefda}.cg-911{background:#fff;color:#a8331f;border:2px solid #a8331f}" +
      ".cg-close{background:none;border:0;color:#524c4f;text-decoration:underline;font:600 .95rem Nunito,system-ui,sans-serif;cursor:pointer;padding:8px;display:block;margin:0 auto}" +
      ".cg-small{font-size:.9rem;color:#524c4f}";
    var s = document.createElement("style"); s.textContent = css; document.head.appendChild(s);
  }

  function show() {
    if (shown) return; shown = true; style();
    var back = document.createElement("div");
    back.className = "cg-back";
    back.setAttribute("role", "alertdialog"); back.setAttribute("aria-modal", "true"); back.setAttribute("aria-labelledby", "cg-h");
    back.innerHTML =
      '<div class="cg-box">' +
      '<h2 id="cg-h">Please reach out for help right now</h2>' +
      "<p>It sounds like you might be going through something really serious. We're glad you're here, and we want you to be safe.</p>" +
      "<p>The Emotional Support Line isn't a crisis service, and we can't help with life-or-death situations. The people at <b>988</b> and <b>911</b> are trained for exactly this, and they're there any time, day or night.</p>" +
      '<div class="cg-btns">' +
      '<a class="cg-988" href="tel:988">Call 988 (Suicide &amp; Crisis Lifeline)</a>' +
      '<a class="cg-txt" href="sms:988">Text 988</a>' +
      '<a class="cg-911" href="tel:911">Call 911 if you or someone else is in danger</a>' +
      "</div>" +
      '<p class="cg-small">Outside the US, please call your local emergency number.</p>' +
      '<button class="cg-close" type="button">Close this message</button>' +
      "</div>";
    document.body.appendChild(back);
    var first = back.querySelector(".cg-988"); if (first) first.focus();
    function close() { back.remove(); shown = false; }
    back.querySelector(".cg-close").addEventListener("click", close);
    document.addEventListener("keydown", function k(e) { if (e.key === "Escape") { close(); document.removeEventListener("keydown", k); } });
  }

  function check(text) {
    if (!text || text.length < 2) return;
    for (var i = 0; i < PATTERNS.length; i++) if (PATTERNS[i].test(text)) { show(); return; }
  }

  // Anything typed into a text box, search box or message field, anywhere on the page
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t && (t.tagName === "TEXTAREA" || (t.tagName === "INPUT" && /^(text|search|)$/i.test(t.type || "")) || t.isContentEditable)) {
      clearTimeout(t._cg); t._cg = setTimeout(function () { check(t.value || t.textContent); }, 600);
    }
  }, true);
  // Arriving with a search phrase in the address (site search, ads, or links)
  try { var q = new URLSearchParams(location.search); q.forEach(function (v) { check(v); }); } catch (e) {}
  // Other scripts (such as the future AI sales guide) can call this with a visitor's message
  window.ESLCrisisCheck = check;
  window.ESLCrisisShow = show;
})();

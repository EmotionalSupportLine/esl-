// Seasonal pop-up for the free 100 Things workbook.
// Shows once per visitor (again after 14 days if closed), after 25 seconds or half a page of scrolling,
// until January 31, 2027. Never on the 100 Things page itself, never after someone has signed up.
(function () {
  if (new Date() > new Date("2027-02-01T00:00:00")) return;
  if (/\/free\/100-things|\/app/.test(location.pathname)) return;
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  if (store.get("esl_100_ok") === "1") return;
  var closed = +store.get("esl_100_closed") || 0;
  if (Date.now() - closed < 14 * 864e5) return;
  var shown = false;

  function build() {
    if (shown) return; shown = true;
    var css = document.createElement("style");
    css.textContent =
      ".p100{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(19,79,83,.55)}" +
      ".p100 .box{position:relative;max-width:520px;width:100%;max-height:92vh;overflow:auto;background:#FCEFDA;border-radius:22px;box-shadow:0 30px 60px -20px rgba(0,0,0,.5);font-family:Nunito,system-ui,sans-serif;color:#1F1C1C}" +
      ".p100 img{display:block;width:100%;height:auto;border-radius:22px 22px 0 0}" +
      ".p100 .in{padding:20px 24px 22px}" +
      ".p100 h2{font:700 1.55rem/1.2 Lora,Georgia,serif;color:#134F53;margin:0 0 8px}" +
      ".p100 p{margin:0 0 12px;line-height:1.5}" +
      ".p100 form{display:flex;flex-wrap:wrap;gap:8px}" +
      ".p100 input[type=email]{flex:1 1 220px;min-height:46px;border:2px solid #e3d2b6;border-radius:999px;padding:0 16px;font:inherit;background:#fff}" +
      ".p100 button[type=submit]{min-height:46px;border:0;border-radius:999px;padding:0 20px;background:#D7783A;color:#fff;font:800 1rem Nunito,system-ui,sans-serif;cursor:pointer}" +
      ".p100 .x{position:absolute;top:10px;right:12px;width:36px;height:36px;border-radius:50%;border:0;background:rgba(255,255,255,.9);font-size:22px;line-height:36px;cursor:pointer;color:#134F53}" +
      ".p100 .small{font-size:.85rem;color:#524C4F;margin:10px 0 0}" +
      ".p100 .dl{display:inline-block;margin-top:4px;background:#134F53;color:#FCEFDA;text-decoration:none;font-weight:800;padding:12px 20px;border-radius:999px}";
    document.head.appendChild(css);
    var wrap = document.createElement("div");
    wrap.className = "p100";
    wrap.setAttribute("role", "dialog"); wrap.setAttribute("aria-modal", "true"); wrap.setAttribute("aria-labelledby", "p100h");
    wrap.innerHTML =
      '<div class="box"><button class="x" type="button" aria-label="Close">×</button>' +
      '<img src="/assets/library/100-things-free.jpg" alt="" width="1200" height="810">' +
      '<div class="in"><h2 id="p100h">Do you feel like you didn’t get enough done this year?</h2>' +
      '<p>You did more than you think. Get the free 100 Things workbook and count again.</p>' +
      '<form action="https://traceesioux.us2.list-manage.com/subscribe/post?u=1518241fc7aee7782d17d61e9&amp;id=bd683fce4d" method="post" data-soft="1" data-tag="100 Things 2026" data-ok="Here it is! Check your inbox too.">' +
      '<input type="email" name="EMAIL" placeholder="Your email" aria-label="Your email" autocomplete="email" required>' +
      '<div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_1518241fc7aee7782d17d61e9_bd683fce4d" tabindex="-1" value=""></div>' +
      '<button type="submit">Send me the workbook</button></form>' +
      '<p class="small">Free. You’ll also get EmoOwl’s Energy Forecast on Sundays. Unsubscribe anytime.</p></div></div>';
    document.body.appendChild(wrap);
    function close() { wrap.remove(); store.set("esl_100_closed", String(Date.now())); document.removeEventListener("keydown", esc); }
    function esc(e) { if (e.key === "Escape") close(); }
    wrap.querySelector(".x").addEventListener("click", close);
    wrap.addEventListener("click", function (e) { if (e.target === wrap) close(); });
    document.addEventListener("keydown", esc);
    var form = wrap.querySelector("form");
    form.addEventListener("esl:signedup", function () {
      store.set("esl_100_ok", "1");
      wrap.querySelector(".in").innerHTML = '<h2>Here’s your workbook</h2><p>We’ve emailed it to you too. Set aside 20 minutes, open your photos and start counting.</p>' +
        '<a class="dl" href="/assets/workbooks/100-things.pdf" target="_blank" rel="noopener">Download the 100 Things workbook</a>';
    });
    wrap.querySelector("input[type=email]").focus({ preventScroll: true });
  }

  setTimeout(build, 25000);
  window.addEventListener("scroll", function onScroll() {
    var h = document.documentElement;
    if ((h.scrollTop + innerHeight) / h.scrollHeight > 0.5) { window.removeEventListener("scroll", onScroll); build(); }
  }, { passive: true });
})();

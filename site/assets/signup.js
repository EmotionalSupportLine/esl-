// Energy Forecast sign-up: sends the email to Mailchimp in the background (JSONP, the same
// method Mailchimp's own embedded forms use), so visitors stay on the page and usually skip
// Mailchimp's "Confirm Humanity" page. If anything goes wrong it falls back to the normal
// Mailchimp page in a new tab.
(function () {
  function note(form) {
    var n = form.nextElementSibling;
    if (n && n.classList && n.classList.contains("note")) return n;
    n = form.querySelector(".signup-msg");
    if (!n) { n = document.createElement("p"); n.className = "note signup-msg"; n.setAttribute("role", "status"); form.appendChild(n); }
    return n;
  }
  function clean(msg) {
    var d = document.createElement("div"); d.innerHTML = msg || ""; var t = d.textContent || "";
    return t.replace(/^\d+ - /, "");
  }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    var action = form.getAttribute("action") || form.action || "";
    if (action.indexOf("list-manage.com/subscribe/post") === -1 || form.dataset.fallback) return;
    e.preventDefault(); e.stopPropagation();
    var msg = note(form), btn = form.querySelector("button[type=submit]");
    var email = (form.querySelector("input[name=EMAIL]") || {}).value || "";
    if (!email) return;
    msg.textContent = "Sending…"; if (btn) btn.disabled = true;
    var cb = "eslmc" + Date.now(), done = false, s = document.createElement("script");
    var params = new URLSearchParams(new FormData(form)).toString();
    var url = action.replace("/subscribe/post?", "/subscribe/post-json?") + "&" + params + "&c=" + cb;
    function finish() { done = true; if (btn) btn.disabled = false; try { delete window[cb]; } catch (x) { window[cb] = undefined; } s.remove(); }
    function fallback() { form.dataset.fallback = "1"; msg.textContent = "Opening the sign-up page in a new tab…"; form.submit(); }
    window[cb] = function (r) {
      finish();
      var text = clean(r && r.msg);
      if (r && r.result === "success") {
        msg.textContent = "Almost there! Check your inbox and click the confirm button. Your first Energy Forecast arrives Sunday.";
        form.reset();
      } else if (/already subscribed/i.test(text)) {
        msg.textContent = "You're already on the list. Watch for EmoOwl's Energy Forecast on Sunday.";
      } else if (/captcha|robot|too many/i.test(text)) {
        fallback();
      } else {
        msg.textContent = text || "That didn't go through. Please check the email address and try again.";
      }
    };
    s.src = url; s.onerror = function () { if (!done) { finish(); fallback(); } };
    setTimeout(function () { if (!done) { finish(); fallback(); } }, 9000);
    document.body.appendChild(s);
  }, true);
})();

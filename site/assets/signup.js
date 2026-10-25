// Energy Forecast and waiting-list sign-ups.
// 1) Our own /api/subscribe (Mailchimp API, no captcha page). 2) If that isn't set up, Mailchimp's
// own form opens in a new tab. Visitors always get a clear message on the page.
(function () {
  function note(form) {
    var n = form.nextElementSibling;
    if (n && n.classList && n.classList.contains("note")) return n;
    n = form.querySelector(".signup-msg");
    if (!n) { n = document.createElement("p"); n.className = "note signup-msg"; n.setAttribute("role", "status"); form.appendChild(n); }
    return n;
  }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    var action = form.getAttribute("action") || form.action || "";
    if (action.indexOf("list-manage.com/subscribe/post") === -1 || form.dataset.fallback) return;
    e.preventDefault(); e.stopPropagation();
    var msg = note(form), btn = form.querySelector("button[type=submit]");
    var val = function (n) { var el = form.querySelector("[name='" + n + "']:checked") || form.querySelector("[name='" + n + "']:not([type=radio])"); return el ? el.value : ""; };
    var email = val("EMAIL");
    if (!email) return;
    var waitlist = !!form.querySelector("[name=SPPRICE]");
    msg.textContent = "Sending…"; if (btn) btn.disabled = true;
    function done(r) { form.dispatchEvent(new CustomEvent("esl:signedup", { bubbles: true, detail: r || {} })); }
    function fallback() {
      if (btn) btn.disabled = false;
      if (form.dataset.soft) { msg.textContent = "Here you go!"; return done({}); } // never block a free gift on a technical hiccup
      form.dataset.fallback = "1"; form.setAttribute("target", "_self");
      msg.textContent = "Taking you to Mailchimp to finish signing up…";
      form.submit();
    }
    fetch("/api/subscribe", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, fname: val("FNAME"), spprice: val("SPPRICE"), freq: val("FREQ") || form.dataset.freq || "weekly", tag: form.dataset.tag || "", hp: val("b_1518241fc7aee7782d17d61e9_bd683fce4d") })
    }).then(function (r) { return r.json(); }).then(function (r) {
      if (btn) btn.disabled = false;
      if (r.fallback) return fallback();
      if (r.error) { msg.textContent = r.error; return; }
      if (r.status === "subscribed") {
        msg.textContent = waitlist ? "Thanks! You're on the waiting list, and we saved your answer." : "You're already on the list, and we've saved your choice.";
      } else {
        msg.textContent = form.dataset.ok || (val("FREQ") === "monthly" ? "Almost there! Check your inbox and click the confirm button. Your first monthly letter arrives at the start of next month." : "Almost there! Check your inbox and click the confirm button. Your first Energy Forecast arrives Sunday.");
      }
      form.reset();
      done(r);
    }).catch(fallback);
  }, true);
})();

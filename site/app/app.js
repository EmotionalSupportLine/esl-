// The Nest. Everything a member tracks lives in this browser's storage, on their device.
(function () {
  const C = window.ESL;
  const KEY = "nest.v1";
  const $ = (s, el = document) => el.querySelector(s);
  const view = $("#view");
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // ---------- storage (on device only) ----------
  let state = { days: {}, settings: {}, member: null, active: null };
  try { state = Object.assign(state, JSON.parse(localStorage.getItem(KEY) || "{}")); } catch (e) {}
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} };
  const dayKey = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = () => (state.days[dayKey()] ||= { earth: 0, sun: 0, extras: {}, words: [] });

  const isMember = () => state.member && state.member.exp > Date.now();
  let memberData = null;

  function toast(msg) {
    const t = document.createElement("div"); t.className = "toast"; t.textContent = msg; t.setAttribute("role", "status");
    document.body.appendChild(t); setTimeout(() => t.remove(), 3200);
  }

  // ---------- membership ----------
  async function api(path, opts = {}) {
    const r = await fetch(path, opts);
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || "Something went wrong. Try again.");
    return data;
  }
  function setMember(d) { state.member = { email: d.email, pass: d.pass, exp: d.exp, code: d.code }; save(); memberData = null; }

  async function handleCheckoutReturn() {
    const p = new URLSearchParams(location.search);
    const sid = p.get("session_id"), k = p.get("k");
    if (!sid && !k) return;
    history.replaceState(null, "", "/app/");
    try {
      const d = await api(`/api/join?session_id=${encodeURIComponent(sid || "")}&k=${encodeURIComponent(k || "")}`);
      setMember(d);
      if (d.next) { state.next = { url: d.next, what: d.what, months: d.guest > 40 ? 3 : 1 }; save(); }
      toast(d.next ? `Your free ${d.guest > 40 ? "3 months" : "month"} in the Nest has started.` : "Welcome to the Nest. You're in.");
    }
    catch (e) { toast(e.message); }
  }

  // After buying a call or reading: a banner that stays until they've opened the booking page
  function bookingBanner() {
    const n = state.next; if (!n || document.getElementById("book-next")) return;
    const b = document.createElement("div"); b.id = "book-next";
    b.style.cssText = "position:sticky;top:0;z-index:50;background:#134F53;color:#FCEFDA;padding:14px 16px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;font-weight:700;text-align:center";
    b.innerHTML = `<span>Thank you! Next, pick the time for your ${n.what === "reading" ? "2-hour Human Design reading" : "support call"}. Your free ${n.months === 3 ? "3 months" : "month"} in the Nest has started.</span><a class="btn btn-sun" href="${esc(n.url)}" target="_blank" rel="noopener">Pick your time</a>`;
    b.querySelector("a").addEventListener("click", () => { state.next = null; save(); setTimeout(() => b.remove(), 300); });
    document.body.prepend(b);
  }

  async function loadMember() {
    if (!isMember()) return null;
    if (memberData) return memberData;
    try {
      memberData = await api("/api/members", { headers: { Authorization: `Bearer ${state.member.pass}` } });
    } catch (e) {
      // Expired pass: try a quiet refresh with the saved email
      try { setMember(await api("/api/restore", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: state.member.email, code: state.member.code }) })); memberData = await api("/api/members", { headers: { Authorization: `Bearer ${state.member.pass}` } }); }
      catch (e2) { state.member = null; save(); return null; }
    }
    return memberData;
  }

  const joinUrl = () => C.links.nestFounding || C.links.nestMonthly || "/#prices";
  function lockCard(what) {
    return `<section class="lock">
      <h2>${what} is for Nest members</h2>
      <p>Join to unlock the Sky, the class library and the member call rate.</p>
      <ul><li>Moon, planets and space weather for where you are</li><li>Year of YES! courses and guided meditations</li><li>Monthly live Community Call</li><li>Calls at $${C.prices.callMember} instead of $${C.prices.callPublic}</li></ul>
      <a class="btn btn-sun" href="${esc(joinUrl())}">Join for $${C.foundingOpen ? C.prices.nestFounding : C.prices.nestMonthly} a month</a>
      <button class="alt" type="button" data-restore>Already a member? Restore access</button>
    </section>`;
  }

  // ---------- timers ----------
  const GOALS = { earth: 30 * 60, sun: 15 * 60 };
  let ticker = null, audio = null;

  function elapsed(kind) {
    const t = today();
    let s = t[kind];
    if (state.active && state.active.kind === kind) s += Math.floor((Date.now() - state.active.start) / 1000);
    return s;
  }
  function stopActive() {
    if (!state.active) return;
    const { kind, start, day } = state.active;
    const add = Math.floor((Date.now() - start) / 1000);
    const d = (state.days[day] ||= { earth: 0, sun: 0, extras: {}, words: [] });
    d[kind] += Math.min(add, 4 * 3600); // a forgotten timer counts for at most 4 hours
    state.active = null; save(); tone(false);
  }
  function toggle(kind) {
    const wasThis = state.active && state.active.kind === kind;
    stopActive();
    if (!wasThis) { state.active = { kind, start: Date.now(), day: dayKey() }; save(); if (state.settings.tone) tone(true); }
    render();
  }
  function tone(on) {
    try {
      if (!on) { if (audio) { audio.ctx.close(); audio = null; } return; }
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.value = 528; g.gain.value = 0.0001; o.connect(g).connect(ctx.destination); o.start();
      g.gain.exponentialRampToValueAtTime(0.05, ctx.currentTime + 2);
      audio = { ctx };
    } catch (e) {}
  }
  const mmss = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  function ring(kind) {
    const s = elapsed(kind), p = Math.min(s / GOALS[kind], 1), r = 46, c = 2 * Math.PI * r;
    return `<div class="ring"><svg viewBox="0 0 104 104"><circle cx="52" cy="52" r="${r}" fill="none" stroke="rgba(252,239,218,.25)" stroke-width="8"/><circle cx="52" cy="52" r="${r}" fill="none" stroke="#fcefda" stroke-width="8" stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - p)}"/></svg><div class="t" data-clock="${kind}">${mmss(s)}<small>of ${GOALS[kind] / 60} min</small></div></div>`;
  }

  // ---------- views ----------
  const EXTRAS = [["soil", "🌱", "Touch soil"], ["tree", "🌳", "Hug a tree"], ["plant", "🪴", "Plant something"], ["eat", "🍎", "Eat homegrown"], ["garden", "🧺", "Garden time"]];
  const WORDS = ["Peace", "Clarity", "Courage", "Rest", "Release", "Abundance", "Love", "Health", "Trust", "Joy", "Patience", "Forgiveness"];

  function weekStrip() {
    const out = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      const rec = state.days[dayKey(d)] || { earth: 0, sun: 0 };
      const mins = (rec.earth + rec.sun) / 60;
      const cls = mins >= 20 ? "full" : mins >= 5 ? "half" : "";
      out.push(`<div class="${i === 0 ? "today" : ""}"><span class="${cls}"></span>${d.toLocaleDateString(undefined, { weekday: "narrow" })}</div>`);
    }
    return out.join("");
  }
  function streak() {
    let n = 0; const d = new Date();
    for (;;) {
      const rec = state.days[dayKey(d)];
      if (rec && rec.earth + rec.sun >= 5 * 60) { n++; d.setDate(d.getDate() - 1); }
      else if (n === 0 && dayKey(d) === dayKey()) { d.setDate(d.getDate() - 1); }
      else break;
    }
    return n;
  }

  function viewToday() {
    const t = today(), m = Sky.moon();
    const hour = new Date().getHours();
    const hi = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
    const s = streak();
    const intention = m.name === "Full moon" || m.name === "New moon" ? `It's a ${m.name.toLowerCase()} tonight, a good night to set water out.` : `Next ${m.waxing ? "full" : "new"} moon: ${m[m.waxing ? "nextFull" : "nextNew"].toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}.`;
    view.innerHTML = `
      <div class="hello"><h1>${hi}</h1><p>${Sky.moonSVG(m, 22, "#d7783a", "rgba(19,79,83,.25)")} ${esc(m.name)}, Moon in ${esc(m.sign)}</p></div>
      <div class="timers">
        <section class="timer earth ${state.active && state.active.kind === "earth" ? "on" : ""}"><h2>Earthing</h2>${ring("earth")}<div class="goal">Bare feet on grass, sand or soil</div><button type="button" data-timer="earth">${state.active && state.active.kind === "earth" ? "Pause" : "Start"}</button></section>
        <section class="timer sun ${state.active && state.active.kind === "sun" ? "on" : ""}"><h2>Morning sun</h2>${ring("sun")}<div class="goal">Light in your eyes before 10 am</div><button type="button" data-timer="sun">${state.active && state.active.kind === "sun" ? "Pause" : "Start"}</button></section>
      </div>
      <section class="card">
        <h2>Little touches today</h2>
        <p class="sub">Tap each time you do one.</p>
        <div class="extras">${EXTRAS.map(([k, e, label]) => `<button type="button" data-extra="${k}"><span class="e" aria-hidden="true">${e}</span>${label}<span class="n">${t.extras[k] ? "×" + t.extras[k] : ""}</span></button>`).join("")}</div>
      </section>
      <section class="card">
        <h2>${s ? `${s}-day streak` : "Your week"}</h2>
        <p class="sub">${s ? "Any day with 5 or more minutes outside counts." : "Five minutes outside starts a streak."}</p>
        <div class="week">${weekStrip()}</div>
      </section>
      <section class="card">
        <h2>Water intention</h2>
        <p class="sub">${esc(intention)} Pick words to hold while you fill a glass or jar.</p>
        <div class="chips">${WORDS.map((w) => `<button type="button" data-word="${w}" aria-pressed="${t.words.includes(w)}">${w}</button>`).join("")}</div>
      </section>
      <section class="card">
        <h2>Tone while you time</h2>
        <p class="sub">Play a soft 528 Hz tone while a timer runs.</p>
        <div class="chips"><button type="button" data-tone aria-pressed="${!!state.settings.tone}">${state.settings.tone ? "Tone on" : "Tone off"}</button></div>
      </section>`;
  }

  async function viewSky() {
    if (!isMember()) { view.innerHTML = lockCard("The Sky"); return; }
    const m = Sky.moon(), pl = Sky.planets(), up = Sky.upcoming(new Date(), 30);
    const fmt = (d) => d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
    const loc = state.settings.place;
    view.innerHTML = `
      <section class="card"><div class="moonbig">${Sky.moonSVG(m, 84, "#fcefda", "#134f53")}<div><div class="name">${esc(m.name)}</div><div class="sub" style="margin:0">${Math.round(m.illum * 100)}% lit, Moon in ${esc(m.sign)}</div><div class="sub" style="margin:4px 0 0">Full moon ${fmt(m.nextFull)}. New moon ${fmt(m.nextNew)}.</div></div></div></section>
      <section class="card"><h2>Your sun today</h2>
        <div id="local">${loc ? `<p class="sub">Loading sunrise and UV for ${esc(loc)}…</p>` : `<p class="sub">Add your location to see sunrise, sunset and UV. It stays on this device.</p><button class="btn btn-night" type="button" data-locate>Use my location</button>`}</div></section>
      <section class="card"><h2>Space weather</h2><div id="kp"><p class="sub">Checking the latest geomagnetic readings…</p></div></section>
      <section class="card"><h2>Planets now</h2><ul class="rows">${pl.map((p) => `<li><span>${p.glyph} ${p.name}${p.retrograde ? '<span class="rx">retrograde</span>' : ""}</span><span>${p.degree}° ${p.sign}</span></li>`).join("")}</ul></section>
      <section class="card"><h2>Next 30 days</h2><ul class="rows">${up.length ? up.map((e) => `<li><span>${esc(e.text)}</span><span>${fmt(e.date)}</span></li>`).join("") : "<li>A quiet month in the sky.</li>"}</ul>
        <p class="note" style="margin-top:10px">Positions are calculated on your device from real astronomy. What they mean for you is for reflection, not prediction.</p></section>`;
    if (loc) loadLocal();
    loadKp();
  }

  async function loadLocal() {
    const el = $("#local"); if (!el) return;
    const { lat, lon, place } = state.settings;
    try {
      const r = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=sunrise,sunset,uv_index_max&timezone=auto&forecast_days=1`);
      const d = (await r.json()).daily;
      const t = (iso) => new Date(iso).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
      const uv = d.uv_index_max[0];
      const tip = uv >= 8 ? "Very strong sun. Get your minutes early or late." : uv >= 3 ? "Good vitamin D sun around midday. A few minutes goes a long way." : "Low UV today. Morning light still helps your sleep rhythm.";
      el.innerHTML = `<ul class="rows"><li><span>Sunrise</span><b>${t(d.sunrise[0])}</b></li><li><span>Sunset</span><b>${t(d.sunset[0])}</b></li><li><span>Highest UV</span><b>${uv}</b></li></ul><p class="sub" style="margin-top:8px">${tip}</p><p class="note">${esc(place)}</p>`;
    } catch (e) { el.innerHTML = `<p class="sub">Couldn't load local sun times. Check your connection and open the Sky again.</p>`; }
  }

  async function loadKp() {
    const el = $("#kp"); if (!el) return;
    try {
      const r = await fetch("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json");
      let rows = await r.json();
      if (Array.isArray(rows[0])) rows = rows.slice(1).map((x) => ({ kp: parseFloat(x[1]) }));
      else rows = rows.map((x) => ({ kp: parseFloat(x.Kp ?? x.kp_index ?? x.kp) }));
      rows = rows.filter((x) => !isNaN(x.kp)).slice(-16);
      const now = rows[rows.length - 1].kp;
      const word = now >= 5 ? "Geomagnetic storm" : now >= 4 ? "Active" : now >= 3 ? "Unsettled" : "Quiet";
      const tip = now >= 5 ? "Some people feel wired or tired during storms. Extra earthing time and an early night can help." : now >= 4 ? "A little more active than usual. Good day for a longer earthing session." : "Calm conditions. Any time is a good time to get outside.";
      el.innerHTML = `<p style="margin:0"><b>${word}</b>, Kp ${now.toFixed(1)}</p><div class="kp" aria-hidden="true">${rows.map((x) => `<span class="${x.kp >= 4 ? "hi" : ""}" style="height:${Math.max(6, (x.kp / 9) * 100)}%"></span>`).join("")}</div><p class="sub">${tip}</p><p class="note">Last two days, every 3 hours. Data from NOAA.</p>`;
    } catch (e) { el.innerHTML = `<p class="sub">Space weather data isn't available right now. Try again later.</p>`; }
  }

  const COVERS = { "Soul-Conomics": "soul-conomics", "Soul vs Ego": "soul-vs-ego", "Time Joy-gasm": "time-joygasm", "Psychic Spring Clean": "psychic-spring-clean", "Joy R.O.I.": "joy-roi", "Harvest": "harvest", "Guided meditations": "meditations", "3-Minute Miracle": "3-minute-miracle", "Psychic Autumn Clearing": "autumn-clearing" };
  const coverFor = (topic) => { const k = Object.keys(COVERS).find((k) => topic.startsWith(k)); return k ? COVERS[k] : ""; };
  async function viewLibrary() {
    if (!isMember()) { view.innerHTML = lockCard("The Library"); return; }
    view.innerHTML = `<p class="sub">Loading your classes…</p>`;
    const d = await loadMember();
    if (!d) { view.innerHTML = lockCard("The Library"); return; }
    const groups = {};
    d.library.forEach((c) => (groups[c.topic] ||= []).push(c));
    view.innerHTML = `<section class="lib"><h2 style="font-size:1.6rem">Library</h2><p class="sub">Watch at your own pace. New classes are added each month.</p>
      ${Object.entries(groups).map(([topic, list]) => `${coverFor(topic) ? `<div class="course"><img src="/assets/covers/${coverFor(topic)}.jpg" alt="" loading="lazy"><h3>${esc(topic)}</h3></div>` : `<h3>${esc(topic)}</h3>`}${list.map((c) => c.url ? `<a href="${esc(c.url)}" target="_blank" rel="noopener">${esc(c.title)}<small>${esc(c.length || "Watch")}</small></a>` : `<div class="soon">${esc(c.title)}<small>Coming soon</small></div>`).join("")}`).join("")}</section>`;
  }

  async function viewCalls() {
    const member = isMember() ? await loadMember() : null;
    const memberLink = member && member.memberBookUrl;
    view.innerHTML = `
      <section class="card"><h2>Talk to a real person</h2>
        <p class="sub">30 minutes, one issue, and a clear next step. Never AI. Calls run ${esc(C.callHours)}.</p>
        ${member ? `<a class="btn btn-sun" style="width:100%" href="${esc(memberLink || C.links.bookCall)}" target="_blank" rel="noopener">Book at the member rate, $${C.prices.callMember}</a><p class="note" style="margin-top:8px">Pay the member rate, then pick your time.</p>`
        : `<a class="btn btn-sun" style="width:100%" href="${esc(C.links.bookCall)}" target="_blank" rel="noopener">Book a call, $${C.prices.callPublic}</a><p class="note" style="margin-top:8px">Members pay $${C.prices.callMember}. <a href="${esc(joinUrl())}">Join the Nest</a></p>`}
      </section>
      ${member ? `<section class="card"><h2>Monthly group call</h2><p class="sub">${esc(member.groupCall)}</p></section>
      <section class="card"><h2>The Support Plan is coming</h2><p class="sub">A monthly plan with calls included, for seasons when you want regular support. Join the waiting list for first access and a founding price.</p><a class="btn btn-ghost" href="/support-plan">Join the waiting list</a></section>` : ""}
      <section class="card"><h2>What to expect</h2><p class="sub">Your supporter calls you at the number you gave when you booked. Have a quiet spot and one thing you want to talk through. If you're in danger or thinking about suicide, call or text 988 instead.</p></section>`;
  }

  function viewAccount() {
    const body = $("#acct-body");
    const m = state.member;
    body.innerHTML = `
      ${isMember() ? `<p>${m.email && m.email !== "member" ? `Signed in as <b>${esc(m.email)}</b>. ` : ""}Member access on this device until ${new Date(m.exp).toLocaleDateString()}. It renews automatically while your membership is active.</p>${m.code ? `<p class="note">Your member code: <b>${esc(m.code)}</b>. Save it to unlock the Nest on another phone.</p>` : ""}
        ${C.links.billingPortal ? `<p><a class="btn btn-ghost" style="width:100%" href="${esc(C.links.billingPortal)}" target="_blank" rel="noopener">Manage or cancel membership</a></p>` : ""}
        <p><button class="btn btn-ghost" style="width:100%" type="button" data-signout>Sign out on this device</button></p>`
      : `<p>You're using the free version.</p><p><a class="btn btn-sun" style="width:100%" href="${esc(joinUrl())}">Join the Nest</a></p><p><button class="btn btn-ghost" style="width:100%" type="button" data-restore>Restore member access</button></p>`}
      <h3 style="margin-top:18px">Your data</h3>
      <p class="note">Your tracking is saved only on this device. Download a backup to move it to a new phone.</p>
      <div class="field"><button class="btn btn-ghost" type="button" data-export>Download backup</button><label class="btn btn-ghost" style="cursor:pointer">Load backup<input type="file" accept="application/json" data-import hidden></label></div>`;
    $("#acct").showModal();
  }

  // ---------- routing ----------
  let tab = "today";
  const views = { today: viewToday, sky: viewSky, library: viewLibrary, calls: viewCalls };
  function render() { views[tab](); }
  function go(t) {
    tab = t;
    document.querySelectorAll("nav.tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === t)));
    render(); window.scrollTo(0, 0);
  }

  // ---------- events ----------
  document.addEventListener("click", (e) => {
    const b = e.target.closest("button, [data-restore]");
    if (!b) return;
    if (b.dataset.tab) return go(b.dataset.tab);
    if (b.dataset.timer) return toggle(b.dataset.timer);
    if (b.dataset.extra) { const t = today(); t.extras[b.dataset.extra] = (t.extras[b.dataset.extra] || 0) + 1; save(); return render(); }
    if (b.dataset.word) { const t = today(); const w = b.dataset.word; t.words = t.words.includes(w) ? t.words.filter((x) => x !== w) : [...t.words, w]; save(); return render(); }
    if ("tone" in b.dataset) { state.settings.tone = !state.settings.tone; save(); if (state.active) tone(state.settings.tone); return render(); }
    if ("restore" in b.dataset) { $("#acct").open && $("#acct").close(); $("#r-msg").textContent = ""; return $("#restore").showModal(); }
    if ("signout" in b.dataset) { state.member = null; memberData = null; save(); $("#acct").close(); toast("Signed out on this device."); return render(); }
    if ("export" in b.dataset) {
      const blob = new Blob([JSON.stringify({ days: state.days, settings: state.settings }, null, 2)], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `nest-backup-${dayKey()}.json`; a.click(); return;
    }
    if ("locate" in b.dataset) {
      if (!navigator.geolocation) return toast("Location isn't available in this browser.");
      b.textContent = "Finding you…";
      navigator.geolocation.getCurrentPosition(async (pos) => {
        state.settings.lat = pos.coords.latitude.toFixed(3); state.settings.lon = pos.coords.longitude.toFixed(3);
        state.settings.place = `Near ${state.settings.lat}, ${state.settings.lon}`; save(); render();
      }, () => { toast("Location was blocked. You can allow it in your browser settings."); render(); }, { timeout: 10000 });
    }
  });
  $("#acct-btn").addEventListener("click", viewAccount);
  document.addEventListener("change", (e) => {
    if (!e.target.matches("[data-import]")) return;
    const f = e.target.files[0]; if (!f) return;
    f.text().then((txt) => { const d = JSON.parse(txt); if (!d.days) throw 0; state.days = Object.assign(state.days, d.days); state.settings = Object.assign(state.settings, d.settings || {}); save(); $("#acct").close(); toast("Backup loaded."); render(); })
      .catch(() => toast("That file isn't a Nest backup."));
  });
  $("#restore-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = $("#r-msg"); msg.textContent = "Checking…";
    try { setMember(await api("/api/restore", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: $("#r-email").value.trim(), code: $("#r-email").value.trim() }) })); $("#restore").close(); toast("You're in. Welcome back."); render(); }
    catch (err) { msg.textContent = err.message; }
  });

  // Live clock for a running timer
  setInterval(() => {
    if (!state.active || tab !== "today") return;
    if (state.active.day !== dayKey()) { stopActive(); render(); return; }
    const el = document.querySelector(`[data-clock="${state.active.kind}"]`);
    if (el) { const s = elapsed(state.active.kind); if (s % 15 === 0) render(); else el.firstChild.textContent = mmss(s); }
  }, 1000);

  handleCheckoutReturn().then(render).then(bookingBanner);
})();

// Sky engine: moon phase, sun/moon/planet signs, retrogrades.
// Runs entirely on the device. Planet math uses JPL's approximate Keplerian
// elements (valid 1800-2050), accurate to well under a degree: plenty for signs.
(function () {
  const D2R = Math.PI / 180, R2D = 180 / Math.PI;
  const norm = (x) => ((x % 360) + 360) % 360;
  const jd = (date) => date.getTime() / 86400000 + 2440587.5;

  const SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
  const GLYPH = { Sun: "☉", Moon: "☽", Mercury: "☿", Venus: "♀", Mars: "♂", Jupiter: "♃", Saturn: "♄", Uranus: "♅", Neptune: "♆", Pluto: "♇" };

  // [a, e, I, L, longPeri, longNode] and rates per Julian century
  const EL = {
    Mercury: [[0.38709927, 0.20563593, 7.00497902, 252.2503235, 77.45779628, 48.33076593], [0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081]],
    Venus: [[0.72333566, 0.00677672, 3.39467605, 181.9790995, 131.60246718, 76.67984255], [0.0000039, -0.00004107, -0.0007889, 58517.81538729, 0.00268329, -0.27769418]],
    Earth: [[1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0], [0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0]],
    Mars: [[1.52371034, 0.0933941, 1.84969142, -4.55343205, -23.94362959, 49.55953891], [0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343]],
    Jupiter: [[5.202887, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909], [-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106]],
    Saturn: [[9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448], [-0.0012506, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794]],
    Uranus: [[19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.9542763, 74.01692503], [-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589]],
    Neptune: [[30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574], [0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664]],
    Pluto: [[39.48211675, 0.2488273, 17.14001206, 238.92903833, 224.06891629, 110.30393684], [-0.00031596, 0.0000517, 0.00004818, 145.20780515, -0.04062942, -0.01183482]],
  };

  function helio(name, T) {
    const [b, r] = EL[name];
    const [a, e, I, L, wb, O] = b.map((v, i) => v + r[i] * T);
    const w = wb - O;
    let M = norm(L - wb); if (M > 180) M -= 360;
    const Mr = M * D2R; let E = Mr + e * Math.sin(Mr);
    for (let k = 0; k < 8; k++) E -= (E - e * Math.sin(E) - Mr) / (1 - e * Math.cos(E));
    const xp = a * (Math.cos(E) - e), yp = a * Math.sqrt(1 - e * e) * Math.sin(E);
    const cw = Math.cos(w * D2R), sw = Math.sin(w * D2R), cO = Math.cos(O * D2R), sO = Math.sin(O * D2R), cI = Math.cos(I * D2R);
    return [(cw * cO - sw * sO * cI) * xp + (-sw * cO - cw * sO * cI) * yp, (cw * sO + sw * cO * cI) * xp + (-sw * sO + cw * cO * cI) * yp];
  }

  function longitude(name, date) {
    const d = jd(date) - 2451545, T = d / 36525, prec = 1.3969 * T; // J2000 -> tropical of date
    if (name === "Moon") {
      const L = 218.316 + 13.176396 * d, M = 134.963 + 13.064993 * d, F = 93.272 + 13.22935 * d, Ms = 357.529 + 0.98560028 * d, Dm = 297.85 + 12.190749 * d;
      return norm(L + 6.289 * Math.sin(M * D2R) + 1.274 * Math.sin((2 * Dm - M) * D2R) + 0.658 * Math.sin(2 * Dm * D2R) - 0.186 * Math.sin(Ms * D2R) - 0.114 * Math.sin(2 * F * D2R));
    }
    const [xe, ye] = helio("Earth", T);
    if (name === "Sun") return norm(Math.atan2(-ye, -xe) * R2D + prec);
    const [x, y] = helio(name, T);
    return norm(Math.atan2(y - ye, x - xe) * R2D + prec);
  }

  const signOf = (lon) => ({ sign: SIGNS[Math.floor(lon / 30)], degree: Math.floor(lon % 30) });

  function planets(date = new Date()) {
    const next = new Date(date.getTime() + 86400000);
    return ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"].map((name) => {
      const lon = longitude(name, date);
      let diff = norm(longitude(name, next) - lon); if (diff > 180) diff -= 360;
      return { name, glyph: GLYPH[name], lon, ...signOf(lon), retrograde: name !== "Sun" && name !== "Moon" && diff < 0 };
    });
  }

  // Sign changes and retrograde stations in the next N days
  function upcoming(date = new Date(), days = 30) {
    const out = [];
    const names = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Sun"];
    let prev = planets(date).filter((p) => names.includes(p.name));
    for (let i = 1; i <= days; i++) {
      const d = new Date(date.getTime() + i * 86400000);
      const cur = planets(d).filter((p) => names.includes(p.name));
      cur.forEach((p, k) => {
        const q = prev[k];
        if (p.sign !== q.sign) out.push({ date: d, text: `${p.name} enters ${p.sign}` });
        if (p.retrograde !== q.retrograde) out.push({ date: d, text: `${p.name} turns ${p.retrograde ? "retrograde" : "direct"}` });
      });
      prev = cur;
    }
    return out;
  }

  const SYN = 29.530588853, NEW_REF = Date.UTC(2000, 0, 6, 18, 14) / 86400000;
  function moon(date = new Date()) {
    const days = date.getTime() / 86400000 - NEW_REF;
    const age = ((days % SYN) + SYN) % SYN;
    const illum = (1 - Math.cos((2 * Math.PI * age) / SYN)) / 2;
    const names = ["New moon", "Waxing crescent", "First quarter", "Waxing gibbous", "Full moon", "Waning gibbous", "Last quarter", "Waning crescent"];
    const name = names[Math.floor(((age / SYN) * 8 + 0.5) % 8)];
    const nextNew = new Date(date.getTime() + (SYN - age) * 86400000);
    const toFull = (SYN / 2 - age + SYN) % SYN;
    const nextFull = new Date(date.getTime() + toFull * 86400000);
    return { age, illum, name, waxing: age < SYN / 2, nextNew, nextFull, sign: signOf(longitude("Moon", date)).sign };
  }

  // Draws a moon as an SVG string. size in px.
  function moonSVG(m, size = 64, light = "#FCEFDA", dark = "rgba(0,0,0,.35)") {
    const r = size / 2, k = Math.cos((2 * Math.PI * m.age) / SYN); // 1 new, -1 full
    const rx = Math.abs(k) * r;
    const litRight = m.waxing;
    const sweepOuter = litRight ? 1 : 0;
    const terminatorSweep = k > 0 ? (litRight ? 0 : 1) : (litRight ? 1 : 0);
    const d = `M${r} 0 A${r} ${r} 0 0 ${sweepOuter} ${r} ${size} A${rx} ${r} 0 0 ${terminatorSweep} ${r} 0Z`;
    return `<svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}" aria-hidden="true"><circle cx="${r}" cy="${r}" r="${r}" fill="${dark}"/><path d="${d}" fill="${light}"/></svg>`;
  }

  window.Sky = { planets, upcoming, moon, moonSVG, SIGNS };
})();

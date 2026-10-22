"""ESL graphics agent: turns a posts.json file into finished, on-brand images.

Usage:  python3 render.py posts.json out/
Each post: {"id": "...", "type": "affirmation|forecast|tip|relatable|myth|cta", ...fields}
Images are 1080x1350 (4:5), which works for Instagram, Facebook and Pinterest.
"""
import asyncio, base64, html, json, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OWL = "data:image/png;base64," + base64.b64encode((HERE / "owl.png").read_bytes()).decode()
LORA = pathlib.Path("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf").as_uri()
LORA_I = pathlib.Path("/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf").as_uri()
SKY_JS = (HERE / "sky.js").read_text()
SITE = "theemotionalsupportline.com"
e = html.escape

CSS = f"""
@font-face {{ font-family: Lora; src: url('{LORA}'); font-weight: 400 700; }}
@font-face {{ font-family: Lora; src: url('{LORA_I}'); font-style: italic; font-weight: 400 700; }}
* {{ box-sizing: border-box; margin: 0; }}
body {{ width: 1080px; height: 1350px; overflow: hidden; font-family: Poppins, sans-serif; }}
.c {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; }}
.paint {{ position: absolute; inset: 0; }}
.foot {{ position: absolute; left: 80px; right: 80px; bottom: 64px; display: flex; align-items: center; gap: 22px; font-size: 30px; font-weight: 600; }}
.foot img {{ width: 92px; height: 92px; object-fit: contain; }}
.foot b {{ display: block; font: 700 34px/1.2 Lora, serif; }}
.serif {{ font-family: Lora, serif; }}
"""

DEFS = """<defs>
<filter id="wash" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="3" seed="SEED"/><feDisplacementMap in="SourceGraphic" scale="46"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .08 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>"""


def foot(color="#fcefda", sub=SITE):
    return f'<div class="foot" style="color:{color}"><img src="{OWL}" alt=""><div><b>The Emotional Support Line</b>{e(sub)}</div></div>'


def flowers(seed):
    # painted orange blossoms in the corners
    return f"""<g filter="url(#wash)">
      <circle cx="960" cy="150" r="120" fill="#d7783a"/><circle cx="1050" cy="300" r="80" fill="#fcab79"/>
      <circle cx="90" cy="1010" r="90" fill="#fcab79" opacity=".9"/><circle cx="1010" cy="1050" r="60" fill="#d7783a" opacity=".85"/>
      <path d="M-40 1350 C200 1180 420 1260 640 1200 C820 1150 960 1220 1120 1160 V1400 H-40Z" fill="#0d3a3d"/>
    </g>
    <g fill="#fff3d6" opacity=".9"><circle cx="960" cy="150" r="22"/><circle cx="1050" cy="300" r="14"/><circle cx="90" cy="1010" r="16"/></g>"""


def affirmation(p, seed):
    return f"""<div class="c" style="background:#134f53">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><path d="M-60 -60 H700 C560 260 820 520 600 820 C460 1010 160 900 -60 1100Z" fill="#1a6468"/></g>
      {flowers(seed)}<rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div style="position:absolute;left:96px;right:120px;top:300px;color:#fcefda">
      <div class="serif" style="font-size:{p.get('size', 84)}px;line-height:1.18;font-weight:600">{e(p['text'])}</div>
    </div>{foot()}</div>"""


def relatable(p, seed):
    return f"""<div class="c" style="background:#fcefda">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><circle cx="980" cy="120" r="210" fill="#7dc2c5" opacity=".55"/><circle cx="80" cy="1260" r="190" fill="#fcab79" opacity=".6"/></g>
      <rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div style="position:absolute;left:96px;right:110px;top:260px;color:#1f1c1c">
      <div class="serif" style="font-size:{p.get('size', 70)}px;line-height:1.22;font-weight:600">{e(p['text'])}</div>
      {f'<div style="margin-top:46px;font-size:36px;line-height:1.45;color:#524c4f">{e(p["sub"])}</div>' if p.get('sub') else ''}
    </div>{foot('#134f53')}</div>"""


def tip(p, seed):
    n, total = p.get("n"), p.get("of")
    badge = f'<div style="font:700 30px Poppins;color:#d7783a;margin-bottom:28px">{n} of {total}</div>' if n else ""
    cover = p.get("cover")
    bg = "#134f53" if cover else "#fff8ec"
    ink = "#fcefda" if cover else "#1f1c1c"
    body = f'<div style="margin-top:40px;font-size:40px;line-height:1.5;color:{"#e9dcc3" if cover else "#524c4f"}">{e(p.get("body", ""))}</div>' if p.get("body") else ""
    swipe = '<div style="position:absolute;right:80px;bottom:90px;font:700 32px Poppins;color:#fcab79">Swipe for more</div>' if cover else ""
    return f"""<div class="c" style="background:{bg}">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><rect x="-40" y="-40" width="1160" height="150" fill="#d7783a"/><circle cx="1000" cy="1300" r="200" fill="{'#1a6468' if cover else '#f6e2c2'}"/></g>
      <rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div style="position:absolute;left:96px;right:110px;top:250px;color:{ink}">{badge}
      <div class="serif" style="font-size:{p.get('size', 76 if cover else 66)}px;line-height:1.15;font-weight:700">{e(p['title'])}</div>{body}
    </div>{(swipe + f'<img src="{OWL}" alt="" style="position:absolute;left:80px;bottom:70px;width:230px">') if cover else foot('#134f53')}</div>"""


def myth(p, seed):
    return f"""<div class="c" style="background:#fcefda">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><path d="M-60 -60 H1140 V560 C800 640 300 520 -60 600Z" fill="#d7783a"/></g>
      <rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div style="position:absolute;left:96px;right:100px;top:120px;color:#fff8ec">
      <div style="font:700 34px Poppins;opacity:.9">Myth</div>
      <div class="serif" style="font-size:62px;line-height:1.18;font-weight:600;margin-top:14px">{e(p['myth'])}</div></div>
    <div style="position:absolute;left:96px;right:100px;top:690px;color:#1f1c1c">
      <div style="font:700 34px Poppins;color:#134f53">What's true</div>
      <div style="font-size:42px;line-height:1.45;margin-top:14px;color:#1f1c1c">{e(p['truth'])}</div></div>
    {foot('#134f53')}</div>"""


def cta(p, seed):
    return f"""<div class="c" style="background:#d7783a">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><circle cx="540" cy="1420" r="560" fill="#fcefda"/><circle cx="1060" cy="40" r="150" fill="#fcab79"/></g>
      <rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div style="position:absolute;left:96px;right:110px;top:170px;color:#fff8ec">
      <div class="serif" style="font-size:{p.get('size', 92)}px;line-height:1.08;font-weight:700">{e(p['title'])}</div>
      <div style="margin-top:36px;font-size:40px;line-height:1.45">{e(p.get('body', ''))}</div></div>
    <img src="{OWL}" alt="" style="position:absolute;left:50%;transform:translateX(-50%);bottom:300px;width:330px">
    <div style="position:absolute;left:0;right:0;bottom:120px;text-align:center;color:#134f53">
      <div style="display:inline-block;background:#134f53;color:#fcefda;font:700 40px Poppins;padding:24px 48px;border-radius:999px">{e(p.get('button', 'Book a 30-minute call'))}</div>
      <div style="margin-top:22px;font:600 32px Poppins">{SITE}</div></div></div>"""


def forecast(p, seed):
    # Real sky data, computed in the page from sky.js for the week starting p["start"]
    return f"""<div class="c" style="background:#134f53">
    <svg class="paint" viewBox="0 0 1080 1350">{DEFS.replace('SEED', str(seed))}
      <g filter="url(#wash)"><path d="M560 -60 H1140 V1410 H620 C560 1100 700 900 600 640 C520 420 680 200 560 -60Z" fill="#e98a49"/>
      <path d="M-60 1180 C300 1120 640 1200 1140 1140 V1410 H-60Z" fill="#0d3a3d"/></g>
      <circle cx="880" cy="240" r="90" fill="#fff0cf"/><rect width="1080" height="1350" filter="url(#grain)"/></svg>
    <div id="moon" style="position:absolute;left:96px;top:120px"></div>
    <div style="position:absolute;left:96px;right:96px;top:320px;color:#fcefda">
      <div style="font:700 32px Poppins;color:#fcab79">The Owl's Forecast</div>
      <div class="serif" style="font-size:62px;line-height:1.1;font-weight:700;margin-top:8px" id="title"></div>
      <div id="phase" style="font-size:36px;margin-top:18px;color:#cfe3e3"></div>
      <div id="events" style="margin-top:44px;background:rgba(13,58,61,.82);border-radius:28px;padding:20px 40px;font-size:36px;width:820px"></div>
      <div class="serif" style="margin-top:40px;font-size:40px;line-height:1.35;font-style:italic;width:820px;background:rgba(13,58,61,.82);border-radius:28px;padding:28px 40px">{e(p.get('prompt', ''))}</div>
    </div>{foot()}
    <script>{SKY_JS}</script>
    <script>
      const start = new Date({json.dumps(p['start'])} + 'T12:00:00');
      const end = new Date(start.getTime() + 6 * 864e5);
      const f = (d, o) => d.toLocaleDateString('en-US', o);
      const m = Sky.moon(start);
      document.getElementById('moon').innerHTML = Sky.moonSVG(m, 170, '#fcefda', 'rgba(0,0,0,.35)');
      document.getElementById('title').textContent = 'Your week, ' + f(start, {{month:'short', day:'numeric'}}) + ' to ' + f(end, {{month:'short', day:'numeric'}});
      document.getElementById('phase').textContent = m.name + ', Moon in ' + m.sign;
      const ev = Sky.upcoming(new Date(start.getTime() - 864e5), 7).filter(x => x.date <= end);
      [[m.nextFull, 'Full moon'], [m.nextNew, 'New moon']].forEach(([d, t]) => {{ if (d >= start && d <= end) ev.push({{date: d, text: t + ' in ' + Sky.moon(d).sign}}); }});
      const ahead = Sky.upcoming(start, 90);
      Sky.planets(start).filter(x => x.retrograde && ['Mercury','Venus','Mars'].includes(x.name)).forEach(x => {{
        const d = ahead.find(a => a.text === x.name + ' turns direct');
        if (!ev.some(a => a.text.startsWith(x.name))) ev.push({{date: null, text: x.name + ' retrograde' + (d ? ' until ' + f(d.date, {{month:'short', day:'numeric'}}) : '')}});
      }});
      ev.sort((a, b) => (a.date || 0) - (b.date || 0));
      const rows = ev.length ? ev.slice(0, 4) : [{{date: null, text: 'A quiet week in the sky. Good for steady habits.'}}];
      document.getElementById('events').innerHTML = rows.map(x => '<div style="display:flex;justify-content:space-between;gap:24px;padding:18px 0;border-bottom:1px solid rgba(252,239,218,.2)"><span>' + x.text + '</span><b style="color:#fcab79;white-space:nowrap">' + (x.date ? f(x.date, {{weekday:'short', month:'short', day:'numeric'}}) : 'All week') + '</b></div>').join('');
    </script></div>"""


TYPES = {"affirmation": affirmation, "relatable": relatable, "tip": tip, "myth": myth, "cta": cta, "forecast": forecast}


async def main(src, out):
    posts = json.loads(pathlib.Path(src).read_text())
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        pg.on("pageerror", lambda err: print("PAGE ERROR:", err))
        for i, p in enumerate(posts):
            slides = p["slides"] if p["type"] == "carousel" else [p]
            for k, s in enumerate(slides):
                s = {**s, "type": s.get("type", "tip")}
                name = f"{p['id']}" + (f"-{k + 1}" if len(slides) > 1 else "") + ".png"
                body = TYPES[s["type"]](s, 3 + i * 7 + k)
                await pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(out / name))
                print("made", name)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))

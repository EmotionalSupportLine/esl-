"""ESL graphics, bright mixed looks. Usage: python3 render2.py posts.json out/

Each post type has its own look so the feed never repeats itself:
  relatable   -> Sunrise Pop (solid warm color, marker highlight on the last words)
  affirmation -> Sticky Note (colored note taped on cream paper)
  cta         -> Bold Color Block (two colors split on a slant, big button)
  myth        -> Myth / Truth split
  carousel    -> Color-block cover, cream numbered slides
  forecast    -> Bright Sky (dawn gradient, real sky data from sky.js)
Colors rotate by post index. Images are 1080x1350 (4:5).
"""
import asyncio, base64, html, json, pathlib, sys
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OWL = "data:image/png;base64," + base64.b64encode((HERE / "owl.png").read_bytes()).decode()
F = pathlib.Path("/usr/share/fonts/truetype/google-fonts")
SKY_JS = (HERE / "sky.js").read_text()
SITE = "theemotionalsupportline.com"
INK = "#1f1c1c"
e = html.escape

CSS = f"""@font-face{{font-family:Lora;src:url('{(F / 'Lora-Variable.ttf').as_uri()}');font-weight:400 700}}
@font-face{{font-family:Lora;font-style:italic;src:url('{(F / 'Lora-Italic-Variable.ttf').as_uri()}');font-weight:400 700}}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;height:1350px;overflow:hidden}}
.c{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Poppins}}
.h{{font-family:Lora;font-weight:700;letter-spacing:-.01em}}
.mark{{background:linear-gradient(transparent 58%,var(--m) 58%,var(--m) 92%,transparent 92%);padding:0 6px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.tag{{font:700 30px Poppins;letter-spacing:.12em;text-transform:uppercase}}
.site{{font:500 30px Poppins}}
.chip{{display:inline-block;font:700 34px Poppins;padding:22px 40px;border-radius:999px}}"""

POP = [("#FFB38A", "#FFE27A"), ("#FFD86B", "#F7A8B8"), ("#9ED8DB", "#FFE27A"), ("#F7C6D0", "#FFD86B")]
NOTES = [("#FFE27A", -2), ("#F7C6D0", 1.5), ("#BFE6E4", -1.5), ("#FFCBA8", 2)]
BLOCKS = [("#E9733A", "#2CA6AB", "#0f2e31"), ("#D85C7A", "#FFD86B", INK), ("#2CA6AB", "#FFB38A", "#13353a"), ("#134F53", "#FFD86B", INK)]
SKIES = [("#FFD3C2", "#FFE6B8", "#FFF6DC"), ("#C8EAE9", "#FFE0C4", "#FFF3D6"), ("#F9C1CF", "#FFD8B0", "#FFF1C9")]


def size_for(text, big, small, long=60):
    return big if len(text) <= long else small


def sticker(x, y, size, rot, ring="#fff"):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;background:{ring};'
            f'transform:rotate({rot}deg);display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(0,0,0,.12)">'
            f'<img src="{OWL}" style="width:78%"></div>')


_POSES = {}


def pose_src(name):
    """A pose from studio/poses/<name>.png as a data URI; falls back to the logo owl."""
    if not name:
        return OWL
    if name not in _POSES:
        f = HERE / "poses" / f"{name}.png"
        _POSES[name] = ("data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()) if f.exists() else OWL
    return _POSES[name]


def owl(x, y, w, rot=0, say=None, bubble_at="left", pose=None):
    """EmoOwl as the hero: big, no badge ring, with an optional speech bubble and a pose."""
    b = ""
    if say:
        bx = "right:" + str(w - 40) + "px" if bubble_at == "left" else "left:" + str(w - 40) + "px"
        tail = "right:-18px" if bubble_at == "left" else "left:-18px"
        b = (f'<div style="position:absolute;{bx};top:-10px;background:#fff;color:#1f1c1c;font:700 34px/1.2 Poppins;padding:22px 30px;'
             f'border-radius:32px;white-space:nowrap;box-shadow:0 10px 24px rgba(0,0,0,.14)">{e(say)}'
             f'<div style="position:absolute;{tail};top:34px;width:0;height:0;border:18px solid transparent;'
             f'border-{"left" if bubble_at == "left" else "right"}-color:#fff"></div></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">{b}'
            f'<img src="{pose_src(pose)}" style="width:{w}px;filter:drop-shadow(0 18px 24px rgba(0,0,0,.18))"></div>')


def marked(text, color, n=3):
    words = text.split()
    n = min(n, max(1, len(words) - 1))
    return e(" ".join(words[:-n])) + f' <span class="mark" style="--m:{color}">' + e(" ".join(words[-n:])) + "</span>"


def relatable(p, i):
    bg, m = POP[i % len(POP)]
    t = p["text"]
    fs = p.get("size") or size_for(t, 108, 88)
    sub = f'<div style="margin-top:44px;font:500 42px/1.4 Poppins;max-width:700px">{e(p["sub"])}</div>' if p.get("sub") else ""
    cta = p.get("cta", "Free Sunday Forecast · link in bio")
    chip = f'<div class="chip" style="position:absolute;left:90px;bottom:170px;background:{INK};color:{bg};font-size:30px">{e(cta)}</div>' if cta else ""
    return f'''<div class="c" style="background:{bg};color:{INK}">
<div class="tag" style="position:absolute;left:90px;top:110px;opacity:.75">{e(p.get("kicker", "Real talk"))}</div>
<div style="position:absolute;left:90px;right:90px;top:210px"><div class="h" style="font-size:{fs}px;line-height:1.05">{marked(t, m)}</div>{sub}</div>
{chip}
{owl(680, 930, 350, -4, p.get("owl", ["You're not alone.", "Been there.", "I hear you.", "Same, friend."][i % 4]), pose=p.get('pose'))}<div class="site" style="position:absolute;left:90px;bottom:90px">{SITE}</div></div>'''


def affirmation(p, i):
    note, rot = NOTES[i % len(NOTES)]
    t = p["text"]
    fs = p.get("size") or size_for(t, 100, 82, 45)
    return f'''<div class="c" style="background:#fbf3e4">
<div class="tag" style="position:absolute;left:90px;top:100px;color:#d7783a">{e(p.get("kicker", "A note for you"))}</div>
<div style="position:absolute;left:110px;right:110px;top:210px;height:780px;background:{note};transform:rotate({rot}deg);box-shadow:0 30px 60px rgba(60,40,20,.18);padding:110px 80px;display:flex;align-items:center">
<div style="position:absolute;left:50%;top:-30px;width:220px;height:70px;margin-left:-110px;background:rgba(255,255,255,.55);transform:rotate(-3deg)"></div>
<div class="h" style="font-size:{fs}px;line-height:1.1;color:{INK}">{e(t)}</div></div>
{owl(680, 30, 340, 6, pose=p.get('pose'))}<div style="position:absolute;left:110px;bottom:118px;color:#134f53"><div style="font:700 34px Poppins">Saved this? Share it with her.</div><div class="site">{SITE}</div></div></div>'''


def cta(p, i):
    c1, c2, ink = BLOCKS[i % len(BLOCKS)]
    t = p["title"]
    fs = p.get("size") or size_for(t, 112, 92, 40)
    return f'''<div class="c" style="background:{c1}">
<div style="position:absolute;inset:0;background:{c2};clip-path:polygon(0 64%,100% 50%,100% 100%,0 100%)"></div>
<div style="position:absolute;left:90px;right:90px;top:140px;color:#fff">
<div class="h" style="font-size:{fs}px;line-height:1.03">{e(t)}</div>
<div style="margin-top:36px;font:500 40px/1.45 Poppins;max-width:860px;opacity:.95">{e(p.get("body", ""))}</div></div>
<div class="chip" style="position:absolute;left:90px;top:1000px;background:{ink};color:#fff;font-size:42px;padding:28px 52px">{e(p.get("button", "Book a 30-minute call"))} &rarr;</div>
{owl(640, 700, 380, -6, p.get("owl", ["I'm listening.", "We've got you.", "Talk to us.", "Real people here."][i % 4]), pose=p.get('pose'))}<div class="site" style="position:absolute;left:90px;bottom:80px;color:{ink}">{e(p.get("foot", SITE))}</div></div>'''


def myth(p, i):
    bg = POP[i % len(POP)][0]
    return f'''<div class="c" style="background:#fff8ec;color:{INK}">
<div style="position:absolute;left:0;right:0;top:0;height:600px;background:{bg}"></div>
<div style="position:absolute;left:90px;right:90px;top:110px">
<div class="tag">Myth</div>
<div class="h" style="font-size:70px;line-height:1.12;margin-top:20px;text-decoration:line-through;text-decoration-thickness:6px;text-decoration-color:rgba(31,28,28,.55)">{e(p["myth"])}</div></div>
<div style="position:absolute;left:90px;right:90px;top:680px">
<div class="tag" style="color:#d7783a">What's true</div>
<div class="h" style="font-size:58px;line-height:1.2;margin-top:20px">{e(p["truth"])}</div></div>
{owl(770, 1050, 260, 4, pose=p.get('pose'))}<div style="position:absolute;left:90px;bottom:90px"><div style="font:700 34px Poppins;color:#134f53">Free Sunday Forecast · link in bio</div><div class="site">{SITE}</div></div></div>'''


def slide(s, i, cover_colors):
    if s.get("cover"):
        c1, c2, ink = cover_colors
        return f'''<div class="c" style="background:{c1}">
<div style="position:absolute;inset:0;background:{c2};clip-path:polygon(0 70%,100% 58%,100% 100%,0 100%)"></div>
<div class="h" style="position:absolute;left:90px;right:90px;top:180px;font-size:{size_for(s["title"], 108, 90, 40)}px;line-height:1.04;color:#fff">{e(s["title"])}</div>
<div class="chip" style="position:absolute;left:90px;top:1060px;background:{ink};color:#fff">Swipe &rarr;</div>
{owl(620, 780, 400, -6, ["Save this one.", "Try #2 first.", "Send to a friend."][i % 3], pose=s.get('pose'))}</div>'''
    c1 = cover_colors[0]
    return f'''<div class="c" style="background:#fff8ec;color:{INK}">
<div style="position:absolute;left:90px;top:120px;width:150px;height:150px;border-radius:50%;background:{c1};color:#fff;display:flex;align-items:center;justify-content:center;font:700 72px Poppins">{s["n"]}</div>
<div style="position:absolute;left:280px;top:170px;font:700 30px Poppins;color:#8a7f78">{s["n"]} of {s["of"]}</div>
<div style="position:absolute;left:90px;right:90px;top:340px">
<div class="h" style="font-size:{size_for(s["title"], 84, 70, 34)}px;line-height:1.1">{e(s["title"])}</div>
<div style="margin-top:40px;font:500 44px/1.5 Poppins;color:#3d3637">{e(s.get("body", ""))}</div></div>
{"" if s["n"] < s["of"] else f'<div class="chip" style="position:absolute;left:90px;bottom:170px;background:{INK};color:#fff">Get the free Sunday Forecast</div>'}
{owl(820, 1050, 210, 6, pose=s.get('pose'))}<div class="site" style="position:absolute;left:90px;bottom:90px;color:#134f53">{SITE}</div></div>'''


def forecast(p, i):
    g1, g2, g3 = SKIES[i % len(SKIES)]
    return f'''<div class="c" style="background:linear-gradient(170deg,{g1} 0%,{g2} 55%,{g3} 100%);color:{INK}">
<div style="position:absolute;right:-140px;top:-140px;width:640px;height:640px;border-radius:50%;background:radial-gradient(circle,#fff7d6 0%,rgba(255,247,214,0) 70%)"></div>
<div id="moon" style="position:absolute;right:110px;top:110px"></div>
<div style="position:absolute;left:90px;right:90px;top:110px">
<div class="tag" style="color:#134f53">The Owl's Forecast</div>
<div class="h" id="title" style="font-size:76px;line-height:1.05;margin-top:16px;max-width:640px"></div>
<div id="phase" style="font:500 36px Poppins;margin-top:16px;color:#3d3637"></div></div>
<div id="events" style="position:absolute;left:90px;right:90px;top:500px;background:rgba(255,255,255,.6);border-radius:28px;padding:16px 40px;font:500 34px Poppins"></div>
<div class="h" style="position:absolute;left:90px;right:90px;top:880px;font-size:46px;line-height:1.3;font-style:italic">{e(p.get("prompt", ""))}</div>
{owl(790, 1060, 250, 4, pose=p.get('pose'))}
<div style="position:absolute;left:90px;bottom:90px"><div style="font:700 34px Poppins;color:#134f53">Get it free every Sunday · link in bio</div><div class="site">{SITE}</div></div>
<script>{SKY_JS}</script>
<script>{{
  const start = new Date({json.dumps(p["start"])} + 'T12:00:00');
  const end = new Date(start.getTime() + 6 * 864e5);
  const f = (d, o) => d.toLocaleDateString('en-US', o);
  const m = Sky.moon(start);
  document.getElementById('moon').innerHTML = Sky.moonSVG(m, 170, '#fff7d6', 'rgba(19,79,83,.55)');
  document.getElementById('title').textContent = 'Your week, ' + f(start, {{month:'short', day:'numeric'}}) + ' to ' + f(end, {{month:'short', day:'numeric'}});
  document.getElementById('phase').textContent = m.name + ', Moon in ' + m.sign;
  const ev = Sky.upcoming(new Date(start.getTime() - 864e5), 7).filter(x => x.date <= end);
  [[m.nextFull, 'Full moon'], [m.nextNew, 'New moon']].forEach(([d, t]) => {{ if (d >= start && d <= end) ev.push({{date: d, text: t + ' in ' + Sky.moon(d).sign}}); }});
  const ahead = Sky.upcoming(start, 90);
  Sky.planets(start).filter(x => x.retrograde && ['Mercury','Venus','Mars'].includes(x.name)).forEach(x => {{
    const d = ahead.find(a => a.text === x.name + ' turns direct');
    if (!ev.some(a => a.text.startsWith(x.name))) ev.push({{date: null, text: x.name + ' retrograde' + (d ? ' until ' + f(d.date, {{month:'short', day:'numeric'}}) : '')}});
  }});
  const PRE = {json.dumps(p.get('events'))};
  if (PRE) {{ ev.length = 0; PRE.forEach(x => ev.push({{date: x.date ? new Date(x.date) : null, text: x.text}})); if ({json.dumps(p.get('phase', ''))}) document.getElementById('phase').textContent = {json.dumps(p.get('phase', ''))}; }}
  ev.sort((a, b) => (a.date || 0) - (b.date || 0));
  const rows = ev.length ? ev.slice(0, 4) : [{{date: null, text: 'A quiet week in the sky'}}];
  document.getElementById('events').innerHTML = rows.map(x => '<div style="display:flex;justify-content:space-between;gap:24px;padding:18px 0;border-bottom:1px solid rgba(19,79,83,.15)"><span>' + x.text + '</span><b style="color:#c4612a;white-space:nowrap">' + (x.date ? f(x.date, {{weekday:'short', month:'short', day:'numeric'}}) : 'All week') + '</b></div>').join('');
}}</script></div>'''


TYPES = {"relatable": relatable, "affirmation": affirmation, "cta": cta, "myth": myth, "forecast": forecast}


async def main(src, out):
    posts = json.loads(pathlib.Path(src).read_text())
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        seen = {}
        for p in posts:
            # Rotate colors per post type, so neighbours of the same type never share a color
            i = seen[p["type"]] = seen.get(p["type"], -1) + 1
            if p["type"] == "carousel":
                colors = BLOCKS[i % len(BLOCKS)]
                pages = [(f"{p['id']}-{k + 1}.png", slide({**s, "pose": p.get("pose")}, i, colors)) for k, s in enumerate(p["slides"])]
            else:
                pages = [(f"{p['id']}.png", TYPES[p["type"]](p, i))]
            for name, body in pages:
                pg = await b.new_page(viewport={"width": 1080, "height": 1350})
                pg.on("pageerror", lambda err: print("PAGE ERROR:", err))
                await pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
                await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(out / name))
                await pg.close()
                print("made", name)
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))

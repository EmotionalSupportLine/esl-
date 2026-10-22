"""Year of YES! course covers in the sunrise palette. Usage: python3 covers.py out_dir"""
import asyncio, pathlib, sys, html
from playwright.async_api import async_playwright

LORA = pathlib.Path("/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf").as_uri()
LORA_I = pathlib.Path("/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf").as_uri()

COURSES = [
    ("soul-conomics", "Soul-Conomics", "Money and your Soul", "7 classes", 3, "coin"),
    ("soul-vs-ego", "Soul vs Ego Smackdown", "Hearing your Soul over the noise", "5 classes", 5, "two"),
    ("time-joygasm", "Time Joy-gasm", "Experiencing your time as pleasure", "7 classes", 9, "clock"),
    ("psychic-spring-clean", "Psychic Spring Clean", "Clear what no longer belongs to you", "5 classes", 13, "leaf"),
    ("joy-roi", "Joy R.O.I.", "Spend your life where the joy returns", "Worksheet", 17, "spiral"),
    ("harvest", "Harvest", "Gather what this year grew in you", "eCourse", 21, "wheat"),
    ("meditations", "Guided Meditations", "Six recordings for releasing and returning", "Audio", 25, "moon"),
]

ICONS = {
    "coin": '<circle cx="540" cy="900" r="150" fill="none" stroke="#5a2e2a" stroke-width="14"/><circle cx="540" cy="900" r="100" fill="none" stroke="#5a2e2a" stroke-width="6" opacity=".7"/>',
    "two": '<circle cx="470" cy="900" r="130" fill="none" stroke="#5a2e2a" stroke-width="12"/><circle cx="610" cy="900" r="130" fill="none" stroke="#c8562f" stroke-width="12"/>',
    "clock": '<circle cx="540" cy="900" r="150" fill="none" stroke="#5a2e2a" stroke-width="12"/><path d="M540 900 V800 M540 900 L620 950" stroke="#5a2e2a" stroke-width="12" stroke-linecap="round"/>',
    "leaf": '<path d="M540 760 C680 820 690 980 540 1060 C390 980 400 820 540 760Z M540 790 V1050" fill="none" stroke="#5a2e2a" stroke-width="12" stroke-linejoin="round"/>',
    "spiral": '<path d="M540 900 m0 0 a20 20 0 1 1 40 0 a60 60 0 1 1 -120 0 a100 100 0 1 1 200 0 a140 140 0 1 1 -280 0" fill="none" stroke="#5a2e2a" stroke-width="10" stroke-linecap="round"/>',
    "wheat": '<path d="M540 1060 V760" stroke="#5a2e2a" stroke-width="10"/>' + "".join(f'<ellipse cx="{540+s*28}" cy="{790+i*48}" rx="22" ry="36" transform="rotate({s*-30} {540+s*28} {790+i*48})" fill="#5a2e2a"/>' for i in range(5) for s in (-1, 1)),
    "moon": '<path d="M600 760 A150 150 0 1 0 600 1040 A115 115 0 1 1 600 760Z" fill="#5a2e2a"/>',
}

def page(title, sub, kind, seed, icon):
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Lora; src: url('{LORA}'); font-weight: 400 700; }}
@font-face {{ font-family: Lora; src: url('{LORA_I}'); font-style: italic; font-weight: 400 700; }}
*{{margin:0;box-sizing:border-box}} body{{width:1080px;height:1400px;overflow:hidden;font-family:Poppins,sans-serif}}
.c{{position:relative;width:1080px;height:1400px;background:#5a2e2a;overflow:hidden}} svg{{position:absolute;inset:0}}
.t{{position:absolute;left:90px;right:90px;top:110px;color:#fff6ea}}
.brand{{font:700 30px Poppins;letter-spacing:.02em;color:#f6c56b}}
h1{{font:700 {96 if len(title) < 16 else 80}px/1.02 Lora,serif;margin-top:22px}}
.sub{{font:italic 500 40px/1.3 Lora,serif;color:#f7d9c4;margin-top:22px;max-width:820px}}
.foot{{position:absolute;left:90px;right:90px;bottom:80px;display:flex;justify-content:space-between;color:#fff6ea;font:600 30px Poppins}}
</style></head><body><div class="c"><svg viewBox="0 0 1080 1400">
<defs><filter id="w" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.009" numOctaves="3" seed="{seed}"/><feDisplacementMap in="SourceGraphic" scale="44"/></filter>
<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<radialGradient id="s" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffe2a3"/><stop offset=".45" stop-color="#f6c56b"/><stop offset=".8" stop-color="#c8562f" stop-opacity=".85"/><stop offset="1" stop-color="#5a2e2a" stop-opacity="0"/></radialGradient></defs>
<g filter="url(#w)"><circle cx="540" cy="900" r="430" fill="url(#s)"/><path d="M-60 1180 C260 1120 620 1190 1140 1130 V1460 H-60Z" fill="#3d1f1c"/></g>
{ICONS[icon]}<rect width="1080" height="1400" filter="url(#g)"/></svg>
<div class="t"><div class="brand">Year of YES!</div><h1>{e(title)}</h1><div class="sub">{e(sub)}</div></div>
<div class="foot"><span>Tracee Sioux</span><span>{e(kind)}</span></div></div></body></html>"""

async def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1400})
        for slug, title, sub, kind, seed, icon in COURSES:
            await pg.set_content(page(title, sub, kind, seed, icon)); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(out / f"{slug}.png"), type="png")
            print("made", slug)
        await b.close()

asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "covers"))

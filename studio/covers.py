"""Year of YES! course covers: one bold poster per course, built to sell.
Usage: python3 covers.py out_dir
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

F = "/usr/share/fonts/truetype/google-fonts/"
FONTS = f"""
@font-face {{ font-family: Lora; src: url('{pathlib.Path(F+'Lora-Variable.ttf').as_uri()}'); font-weight: 400 700; }}
@font-face {{ font-family: Lora; src: url('{pathlib.Path(F+'Lora-Italic-Variable.ttf').as_uri()}'); font-style: italic; font-weight: 400 700; }}
@font-face {{ font-family: Poppins; src: url('{pathlib.Path(F+'Poppins-Bold.ttf').as_uri()}'); font-weight: 700; }}
@font-face {{ font-family: Poppins; src: url('{pathlib.Path(F+'Poppins-Medium.ttf').as_uri()}'); font-weight: 500; }}
"""
BASE = FONTS + """
*{margin:0;box-sizing:border-box} body{width:1080px;height:1400px;overflow:hidden}
.c{position:relative;width:1080px;height:1400px;overflow:hidden;font-family:Poppins,sans-serif}
.art{position:absolute;inset:0}
.badge{position:absolute;right:56px;top:56px;width:200px;height:200px;border-radius:50%;display:grid;place-items:center;transform:rotate(12deg);
  font:italic 700 44px/1 Lora,serif;text-align:center;box-shadow:0 18px 40px -18px rgba(0,0,0,.5)}
.promise{position:absolute;left:80px;right:80px;font:italic 600 46px/1.25 Lora,serif}
.foot{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font:500 32px Poppins}
.foot b{font-weight:700}
.grain{position:absolute;inset:0;pointer-events:none}
"""
GRAIN = """<svg class="grain" viewBox="0 0 1080 1400"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4"/>
<feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter><rect width="1080" height="1400" filter="url(#g)"/></svg>"""


def badge(bg, fg, pos='top:56px'):
    return f'<div class="badge" style="{pos};background:{bg};color:{fg}">Year of<br>YES!</div>'


def foot(color, fmt):
    return f'<div class="foot" style="color:{color}"><span>with <b>Tracee Sioux</b></span><span>{fmt}</span></div>'


def smackdown():
    return f"""<div class="c" style="background:#1d1b2e">
<svg class="art" viewBox="0 0 1080 1400"><polygon points="0,0 640,0 440,1400 0,1400" fill="#f6c56b"/><polygon points="640,0 1080,0 1080,1400 440,1400" fill="#c8302f"/>
<g opacity=".18" fill="#fff">{''.join(f'<polygon points="540,820 {540+900*__import__("math").cos(a/12*6.283)},{820+900*__import__("math").sin(a/12*6.283)} {540+900*__import__("math").cos((a+.35)/12*6.283)},{820+900*__import__("math").sin((a+.35)/12*6.283)}"/>' for a in range(12))}</g>
<circle cx="540" cy="820" r="140" fill="#1d1b2e"/><text x="540" y="862" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="120" fill="#fff">VS</text></svg>
<div style="position:absolute;left:70px;top:330px;font:700 170px/0.9 Poppins;color:#1d1b2e">SOUL</div>
<div style="position:absolute;right:70px;top:960px;font:700 170px/0.9 Poppins;color:#fff;text-align:right">EGO</div>
<div style="position:absolute;left:-20px;right:-20px;top:1130px;background:#1d1b2e;color:#f6c56b;transform:rotate(-4deg);padding:18px 0;text-align:center;font:700 92px/1 Poppins;letter-spacing:.04em">SMACKDOWN</div>
<div class="promise" style="top:90px;color:#1d1b2e;right:300px">Learn which voice is talking, and which one to trust.</div>
{badge('#fff','#c8302f')}{foot('#fff','5 rounds of video')}{GRAIN}</div>"""


def joygasm():
    rays = ''.join(f'<rect x="535" y="380" width="10" height="120" rx="5" fill="#f6c56b" transform="rotate({i*30} 540 700)"/>' for i in range(12))
    return f"""<div class="c" style="background:#e5457a">
<svg class="art" viewBox="0 0 1080 1400"><circle cx="540" cy="700" r="430" fill="#f2668f"/>{rays}
<circle cx="540" cy="700" r="240" fill="#fff4e2"/><path d="M540 700 V560 M540 700 L640 760" stroke="#e5457a" stroke-width="22" stroke-linecap="round"/>
<circle cx="540" cy="700" r="16" fill="#e5457a"/></svg>
<div style="position:absolute;left:80px;top:96px;font:italic 700 96px/1 Lora,serif;color:#fff4e2">Time</div>
<div style="position:absolute;left:70px;top:190px;font:700 150px/0.92 Poppins;color:#f6c56b;letter-spacing:-.01em">JOY-GASM</div>
<div class="promise" style="top:1000px;color:#fff4e2;text-align:center">Stop managing your time.<br>Start enjoying it.</div>
{badge('#f6c56b','#5a2e2a','top:auto;bottom:140px')}{foot('#fff4e2','7 video classes')}{GRAIN}</div>"""


def soulconomics():
    return f"""<div class="c" style="background:#0f4f3f">
<svg class="art" viewBox="0 0 1080 1400"><circle cx="540" cy="760" r="330" fill="#d9a441"/><circle cx="540" cy="760" r="290" fill="none" stroke="#f6d68a" stroke-width="10"/>
<path d="M540 910 C430 830 390 760 430 700 C460 655 520 660 540 705 C560 660 620 655 650 700 C690 760 650 830 540 910Z" fill="#0f4f3f"/>
<path d="M540 1090 V1240 M540 1170 C600 1140 640 1150 660 1110 C610 1100 570 1120 540 1170 M540 1200 C480 1170 440 1180 420 1140 C470 1130 510 1150 540 1200" stroke="#7fd1a8" stroke-width="10" fill="#7fd1a8"/></svg>
<div style="position:absolute;left:76px;top:96px;font:700 128px/0.95 Poppins;color:#f6d68a">SOUL-<br>CONOMICS</div>
<div class="promise" style="top:380px;color:#e8f5ee;right:120px">Make money in a way that feels like you.</div>
{badge('#f6d68a','#0f4f3f','top:auto;bottom:140px')}{foot('#e8f5ee','7 classes')}{GRAIN}</div>"""


def springclean():
    sparkle = lambda x, y, s: f'<path d="M{x} {y-s} Q{x} {y} {x+s} {y} Q{x} {y} {x} {y+s} Q{x} {y} {x-s} {y} Q{x} {y} {x} {y-s}Z" fill="#fff"/>'
    return f"""<div class="c" style="background:#bfe8d6">
<svg class="art" viewBox="0 0 1080 1400"><rect x="250" y="520" width="580" height="620" rx="14" fill="#7cc6f0"/><circle cx="660" cy="680" r="80" fill="#fff3b0"/>
<path d="M250 1000 C400 940 560 1010 830 960 V1140 H250Z" fill="#7fc79a"/>
<rect x="250" y="520" width="580" height="620" rx="14" fill="none" stroke="#134f53" stroke-width="22"/><path d="M540 520 V1140 M250 830 H830" stroke="#134f53" stroke-width="14"/>
<path d="M230 500 C120 700 190 900 110 1140 L250 1140 L250 500Z" fill="#f28fa0"/><path d="M850 500 C980 640 900 900 990 1100 L830 1140 L830 500Z" fill="#f28fa0"/>
{sparkle(180,430,40)}{sparkle(910,420,30)}{sparkle(960,1230,36)}{sparkle(140,1250,26)}</svg>
<div style="position:absolute;left:76px;top:96px;font:700 100px/0.98 Poppins;color:#134f53">PSYCHIC<br>SPRING CLEAN</div>
<div class="promise" style="top:1160px;color:#134f53;right:320px">Clear out the energy that isn't yours.</div>
{badge('#134f53','#fff','top:auto;bottom:140px')}{foot('#134f53','5 video classes').replace('bottom:64px','bottom:40px')}{GRAIN}</div>"""


def joyroi():
    return f"""<div class="c" style="background:#ffc93c">
<svg class="art" viewBox="0 0 1080 1400"><path d="M120 1080 H960 M120 1080 V560" stroke="#1f2a5a" stroke-width="12" stroke-linecap="round"/>
<path d="M140 1020 L330 940 L480 970 L660 800 L800 720" fill="none" stroke="#e5457a" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="860" cy="660" r="96" fill="#fff4e2" stroke="#1f2a5a" stroke-width="12"/><path d="M820 680 Q860 720 900 680" fill="none" stroke="#1f2a5a" stroke-width="12" stroke-linecap="round"/>
<circle cx="830" cy="640" r="10" fill="#1f2a5a"/><circle cx="890" cy="640" r="10" fill="#1f2a5a"/></svg>
<div style="position:absolute;left:76px;top:96px;font:700 176px/0.9 Poppins;color:#1f2a5a">JOY<br>R.O.I.</div>
<div class="promise" style="top:1140px;color:#1f2a5a">Put your hours where the joy comes back.</div>
{badge('#1f2a5a','#ffc93c')}{foot('#1f2a5a','Workbook').replace('bottom:64px','bottom:40px')}{GRAIN}</div>"""


def harvest():
    stalk = lambda x, r: f'<g transform="rotate({r} {x} 1180)"><path d="M{x} 1180 V760" stroke="#f6c56b" stroke-width="10"/>' + ''.join(f'<ellipse cx="{x+s*24}" cy="{790+i*44}" rx="20" ry="34" transform="rotate({s*-28} {x+s*24} {790+i*44})" fill="#f6c56b"/>' for i in range(6) for s in (-1, 1)) + '</g>'
    return f"""<div class="c" style="background:#4a1f3d">
<svg class="art" viewBox="0 0 1080 1400"><circle cx="540" cy="640" r="250" fill="#e9893a"/><circle cx="540" cy="640" r="250" fill="#f6c56b" opacity=".35"/>
<path d="M0 1180 C300 1120 760 1150 1080 1110 V1400 H0Z" fill="#2c1226"/>{stalk(470,-14)}{stalk(540,0)}{stalk(610,14)}</svg>
<div style="position:absolute;left:76px;top:96px;font:700 156px/0.9 Poppins;color:#f6c56b">HARVEST</div>
<div class="promise" style="top:290px;color:#f7d9c4;right:300px">Gather what this year grew in you.</div>
{badge('#f6c56b','#4a1f3d','top:auto;bottom:140px')}{foot('#f7d9c4','eCourse')}{GRAIN}</div>"""


def meditations():
    stars = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' for x, y, r in [(150,520,4),(260,700,3),(880,520,5),(960,800,3),(820,940,4),(200,980,3),(700,460,3),(400,430,2)])
    return f"""<div class="c" style="background:#2b2a6b">
<svg class="art" viewBox="0 0 1080 1400"><circle cx="540" cy="760" r="320" fill="#3d3b8e"/>{stars}
<path d="M620 520 A250 250 0 1 0 620 1000 A190 190 0 1 1 620 520Z" fill="#e6d7ff"/></svg>
<div style="position:absolute;left:76px;top:96px;font:italic 700 104px/1 Lora,serif;color:#e6d7ff">Come home<br>to yourself</div>
<div class="promise" style="top:1130px;color:#fff;font-style:normal;font-family:Poppins;font-weight:500;font-size:40px">Six guided meditations for releasing, completing and remembering you matter.</div>
{badge('#e6d7ff','#2b2a6b')}{foot('#e6d7ff','Audio').replace('bottom:64px','bottom:40px')}{GRAIN}</div>"""


COVERS = {"soul-vs-ego": smackdown, "time-joygasm": joygasm, "soul-conomics": soulconomics, "psychic-spring-clean": springclean,
          "joy-roi": joyroi, "harvest": harvest, "meditations": meditations}


async def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1400})
        for slug, fn in COVERS.items():
            await pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}</style></head><body>{fn()}</body></html>")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(out / f"{slug}.png"))
            print("made", slug)
        await b.close()

asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "covers"))

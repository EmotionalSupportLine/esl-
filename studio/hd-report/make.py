"""Neutrino report pages (cover, welcome, next steps) for the free Starter and paid Deep reports.
US Letter at 150 dpi (1275x1650). Run: python3 make.py"""
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
HERE = pathlib.Path(__file__).parent; POSES = HERE.parent / "poses"
F = pathlib.Path("/usr/share/fonts/truetype/google-fonts")
def img(n): return "data:image/png;base64," + base64.b64encode((POSES / f"{n}.png").read_bytes()).decode()
CSS = f"""@font-face{{font-family:Lora;src:url('{(F/'Lora-Variable.ttf').as_uri()}');font-weight:400 700}}
@font-face{{font-family:Lora;font-style:italic;src:url('{(F/'Lora-Italic-Variable.ttf').as_uri()}');font-weight:400 700}}
@font-face{{font-family:P;src:url('{(F/'Poppins-Regular.ttf').as_uri()}')}}@font-face{{font-family:P;font-weight:500;src:url('{(F/'Poppins-Medium.ttf').as_uri()}')}}@font-face{{font-family:P;font-weight:700;src:url('{(F/'Poppins-Bold.ttf').as_uri()}')}}
*{{box-sizing:border-box;margin:0}} body{{width:1275px;height:1650px;overflow:hidden;font-family:P,sans-serif;color:#1f1c1c}}
.pg{{position:relative;width:1275px;height:1650px;overflow:hidden;background:#FCEFDA}}
h1,h2,.serif{{font-family:Lora;font-weight:700;color:#134F53}}
.tag{{font:700 26px P;letter-spacing:.18em;text-transform:uppercase;color:#D7783A}}
.foot{{position:absolute;left:110px;right:110px;bottom:70px;display:flex;justify-content:space-between;font:500 24px P;color:#134F53;border-top:2px solid #e7cfa9;padding-top:22px}}
p,li{{font-size:31px;line-height:1.55}} li{{margin:0 0 18px}}
.box{{background:#fff8ec;border-radius:36px;padding:44px 52px;border:2px solid #f0d9b8}}"""
def cover(kind, sub, pose, extra):
    return f"""<div class=pg style="background:linear-gradient(170deg,#134F53 0%,#1a6e72 55%,#2CA6AB 100%)">
<svg width=1275 height=1650 style="position:absolute;inset:0;opacity:.5">{''.join(f'<circle cx="{(i*397)%1275}" cy="{(i*223)%900}" r="{2+(i%3)}" fill="#FCEFDA"/>' for i in range(60))}</svg>
<div style="position:absolute;left:110px;top:150px;right:110px;color:#FCEFDA">
<div class=tag style="color:#FCAB79">The Emotional Support Line</div>
<h1 style="color:#FCEFDA;font-size:118px;line-height:1.02;margin:34px 0 26px">Your Human Design<br><em style="font-weight:600;color:#FCAB79">{kind}</em></h1>
<p style="font-size:38px;color:#e9f4f2;max-width:900px">{sub}</p></div>
<div style="position:absolute;left:110px;top:760px;width:1055px;height:150px;border:3px dashed rgba(252,239,218,.55);border-radius:28px;display:flex;align-items:center;padding:0 40px;color:rgba(252,239,218,.75);font:500 30px P">Prepared for: (add Neutrino's name field here)</div>
<img src="{img(pose)}" style="position:absolute;right:90px;bottom:200px;width:560px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.35))">
<div style="position:absolute;left:110px;bottom:230px;color:#FCEFDA;font:500 28px P;max-width:520px;line-height:1.5">{extra}</div>
<div class=foot style="color:#FCEFDA;border-color:rgba(252,239,218,.35)"><span>theemotionalsupportline.com</span><span>For reflection, not prediction</span></div></div>"""
def welcome(kind, intro, order, pose):
    return f"""<div class=pg><div style="position:absolute;left:110px;right:110px;top:120px">
<div class=tag>Start here</div><h1 style="font-size:84px;margin:20px 0 34px">Welcome to your chart</h1>
<p style="max-width:860px">{intro}</p>
<div class=box style="margin:44px 0 0"><h2 style="font-size:44px;margin-bottom:22px">How to read this {kind}</h2><ol style="padding-left:40px">{''.join(f'<li>{x}</li>' for x in order)}</ol></div>
<div style="margin-top:44px;display:flex;gap:40px;align-items:center"><img src="{img(pose)}" style="width:230px;flex:none"><p style="font-family:Lora;font-style:italic;font-size:34px;color:#134F53">Human Design isn't science and it doesn't predict anything. Use it like a mirror: keep what rings true, and let the rest go.</p></div>
</div><div class=foot><span>The Emotional Support Line</span><span>theemotionalsupportline.com</span></div></div>"""
def nextsteps(lead):
    rows=[("Get EmoOwl's free Energy Forecast","Every Sunday: the week's moon, sky and Human Design gates, plus one question to sit with.","theemotionalsupportline.com/#forecast"),
          ("Live your design every day in the Nest","Morning sun and earthing timers, the sky for where you are, Year of YES! courses and a monthly group call. $19 a month.","theemotionalsupportline.com/#nest"),
          ("Talk it through with a real person","A 30-minute support call: one issue, a calm listener, and a clear next step. $75, or $50 for Nest members.","theemotionalsupportline.com/#calls"),
          ("Build a year around your design","Year of YES! Coaching with Tracee Sioux: two hours a month, one year, guided by your chart. By application.","theemotionalsupportline.com/year-of-yes")]
    return f"""<div class=pg><div style="position:absolute;left:110px;right:110px;top:120px">
<div class=tag>What now?</div><h1 style="font-size:84px;margin:20px 0 26px">Your next step</h1><p style="max-width:760px;margin-bottom:34px">{lead}</p>
{''.join(f'<div class=box style="margin:0 0 20px;padding:28px 46px"><h2 style="font-size:40px;margin-bottom:8px">{t}</h2><p style="font-size:28px">{d}</p><p style="font:700 26px P;color:#D7783A;margin-top:8px">{u}</p></div>' for t,d,u in rows)}
</div>
<img src="{img('heart-hug')}" style="position:absolute;right:100px;top:90px;width:220px">
<div class=foot style="flex-direction:column;gap:6px"><span>Not therapy and not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US) or call 911.</span></div></div>"""
PAGES = {
 "starter-1-cover": cover("Starter Report", "The essentials of how you're built: your type, your strategy and how you make your best decisions.", "bodygraph", "A free gift from EmoOwl,<br>the two owls of The Emotional Support Line."),
 "starter-2-welcome": welcome("Starter Report", "This short report covers the parts of Human Design most people find useful first. Read it slowly, and notice what feels familiar.",
   ["<b>Your Type</b>: how your energy works best.","<b>Your Strategy</b>: the simplest way to meet life with less resistance.","<b>Your Authority</b>: how you're built to make decisions. Many people find this the most useful page.","<b>Your Profile</b>: the role you tend to play.","Then look at your chart and the Centers whenever you're curious."], "reading"),
 "starter-3-next": nextsteps("Want to go deeper? Here's how to keep exploring your design, and get support when life gets heavy."),
 "deep-1-cover": cover("Deep Report", "Your full design: type, strategy, authority, profile, definition, incarnation cross, centers and channels.", "human-design-book", "Prepared for you by<br>The Emotional Support Line."),
 "deep-2-welcome": welcome("Deep Report", "This is your full chart, explained. There's a lot here, so don't try to take it in all at once. Start with the essentials and come back to the rest over the coming weeks.",
   ["<b>Start with Type, Strategy and Authority.</b> They're the foundation for everything else.","<b>Then Profile, Definition and Incarnation Cross</b>: your role, how your energy connects, and your life theme.","<b>Then your Centers and Channels</b>: where you're consistent, where you're open, and the gifts you were born with.","<b>Read one section a day</b>, and write down a sentence or two about what you notice."], "starry-cloak"),
 "deep-3-next": nextsteps("You've met your design. Here's how to live it, with support whenever you need it."),
}
async def main():
    out = HERE / "pages"; out.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width":1275,"height":1650})
        for name, body in PAGES.items():
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{body}</body></html>"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(out / f"{name}.png")); print("made", name)
        await b.close()
asyncio.run(main())

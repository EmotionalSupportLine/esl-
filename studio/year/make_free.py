"""Builds the two free downloads: site/free/moon-calendar-2027.html and site/free/earthing-checklist.html (printable pages)."""
import json, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parents[2]


def link(slug, text):
    """Link to a blog post only once it's live; until then, point to the Energy Forecast."""
    if (ROOT / "site/blog" / f"{slug}.html").exists() or (ROOT / "site/blog" / slug / "index.html").exists():
        return f'<a class="btn btn-ghost" href="/blog/{slug}">{text}</a>'
    return '<a class="btn btn-ghost" href="/forecast/">Read this week\'s Energy Forecast</a>'
cal = json.loads(pathlib.Path("/home/claude/work/mooncal.json").read_text()) if pathlib.Path("/home/claude/work/mooncal.json").exists() else json.loads((ROOT / "studio/year/mooncal-2027.json").read_text())
(ROOT / "studio/year/mooncal-2027.json").write_text(json.dumps(cal, indent=1))
Q_NEW = {"Capricorn": "What steady habit do I want to build, one small step at a time?", "Aquarius": "Where do I want to be more fully myself, even if it's unusual?", "Pisces": "What would I do if I trusted that rest is allowed?", "Aries": "What brave first step have I been putting off?", "Taurus": "What would make my everyday life feel more nourishing?", "Gemini": "What am I curious about right now?", "Cancer": "What would help me feel more at home in my own life?", "Leo": "Where do I want to let my light be seen?", "Virgo": "What small change would make my days run more smoothly?", "Libra": "Where am I giving more than I'm receiving?", "Scorpio": "What am I ready to transform, not just tolerate?", "Sagittarius": "What do I hope for, really?"}
Q_FULL = {"Capricorn": "What responsibility am I ready to put down?", "Aquarius": "Which group or community do I want to belong to more fully?", "Pisces": "Where do I need compassion instead of more effort?", "Aries": "What do I need the courage to finish?", "Taurus": "What does my body need more of?", "Gemini": "What conversation is complete, or needs to happen?", "Cancer": "What do I need to feel safe and cared for?", "Leo": "What am I proud of that I haven't celebrated?", "Virgo": "What everyday habit is quietly draining me?", "Libra": "Which relationship needs more balance?", "Scorpio": "What truth am I ready to stop avoiding?", "Sagittarius": "Where do I feel most free?"}
HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t} | The Emotional Support Line</title><meta name="description" content="{d}"><link rel="icon" href="/assets/owl-128.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/brand.css"><link rel="stylesheet" href="/assets/blog.css">
<style>
.free {{ max-width: 860px; padding: 24px 0 60px; }}
.free table {{ width: 100%; border-collapse: collapse; margin: 18px 0; font-size: .98rem; }}
.free th, .free td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }}
.free th {{ font: 700 1rem var(--serif); color: var(--night); }}
.free .new td:first-child::before {{ content: "● "; color: var(--night); }}
.free .full td:first-child::before {{ content: "○ "; color: var(--orange); }}
.free .ecl {{ display: inline-block; background: var(--sun); color: var(--night-2); font-weight: 800; font-size: .8rem; padding: 2px 8px; border-radius: 999px; margin-left: 6px; }}
.free .q {{ font-style: italic; color: var(--ink-2); }}
.tools {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 14px 0; }}
.tracker {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; margin: 14px 0; }}
.tracker div {{ border: 2px solid var(--teal-light); border-radius: 12px; aspect-ratio: 1; display: flex; align-items: flex-start; justify-content: flex-start; padding: 6px 8px; font-weight: 800; color: var(--night); background: #fff; }}
.check li {{ margin: 8px 0; list-style: none; }} .check li::before {{ content: "☐ "; font-size: 1.2em; color: var(--night); }}
.check {{ padding-left: 0; }}
@media print {{ .crisis, header.top, footer, .tools, .signup, nav {{ display: none !important; }} body {{ background: #fff; }} .free {{ padding: 0; }} .sticker {{ filter: none; }} }}
</style></head><body>
<div class="crisis">Not a crisis line. If you're in danger or thinking about suicide, call or text <a href="tel:988">988</a> (US) or your local emergency number.</div>
<div class="wrap"><header class="top"><a class="brand" href="/"><img src="/assets/owl-128.png" alt=""><span>The Emotional<br>Support Line</span></a>
<nav class="links" aria-label="Main"><a href="/blog/">Blog</a><a href="/forecast/">Forecast</a><a class="btn btn-sun" href="/#calls">Book a call</a></nav></header></div><main>"""
SIGNUP = ('<aside class="signup"><img src="/assets/owls/telescope.webp" alt="" width="96" height="96"><div><h2>Get EmoOwl\'s Energy Forecast, free every Sunday</h2>'
          '<p>Every moon on this page, plus the week\'s sky and one question to sit with, in your inbox.</p>'
          '<form class="field" action="https://traceesioux.us2.list-manage.com/subscribe/post?u=1518241fc7aee7782d17d61e9&amp;id=bd683fce4d" method="post" target="_blank">'
          '<input type="email" name="EMAIL" placeholder="Your email" aria-label="Your email" required><div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_1518241fc7aee7782d17d61e9_bd683fce4d" tabindex="-1" value=""></div><button class="btn btn-sun" type="submit">Send me the Forecast</button></form></div></aside>')
FOOT = '</main><footer><div class="wrap"><span>© 2026 The Emotional Support Line</span><span><a href="/blog/">Blog</a> &nbsp; <a href="/terms.html">Terms</a> &nbsp; <a href="/privacy.html">Privacy</a></span></div></footer><script src="/assets/signup.js" defer></script><script src="/assets/popup-100.js" defer></script><script src="/assets/crisis-guard.js" defer></script></body></html>'
rows = []
for m in cal:
    q = (Q_NEW if m["kind"] == "new" else Q_FULL)[m["sign"]]
    label = ("New moon" if m["kind"] == "new" else f'Full moon, the {m["name"]}') + f' in {m["sign"]}'
    ecl = f'<span class="ecl">{m["eclipse"]}</span>' if m["eclipse"] else ""
    rows.append(f'<tr class="{m["kind"]}"><td>{html.escape(m["when"])}</td><td><b>{html.escape(label)}</b>{ecl}<div class="q">{html.escape(q)}</div></td></tr>')
moon = HEAD.format(t="The 2027 Moon Calendar", d="Every new moon, full moon and eclipse of 2027 in Mountain time, with a reflection question for each. Free and printable.") + f"""
<section class="wrap free"><div class="index-head"><div><p class="kicker"><a href="/">Free from The Emotional Support Line</a></p><h1>The 2027 Moon Calendar</h1>
<p class="lede">Every new moon, full moon and eclipse of 2027, in US Mountain time, with one reflection question for each. New moons are for beginnings, full moons for finishing and letting go.</p></div>
<img class="sticker hero-owl" src="/assets/owls/moon-phases.webp" alt="" width="200" height="200"></div>
<div class="tools"><button class="btn btn-sun" onclick="window.print()">Print or save as PDF</button>{link("new-moon-intentions", "How to use the new moon")}</div>
<table><thead><tr><th>When (Mountain time)</th><th>Moon and a question to sit with</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p class="note"><b>Mercury retrograde in 2027:</b> February 9 to March 3, June 10 to July 4, and October 7 to October 28. Sky dates are real astronomy, calculated for 2027. What they mean for you is a prompt for reflection, never a prediction.</p>
{SIGNUP}</section>""" + FOOT
(ROOT / "site/free/moon-calendar-2027.html").write_text(moon)
days = "".join(f"<div>{i}</div>" for i in range(1, 15))
earth = HEAD.format(t="The Earthing Starter Checklist", d="A free, printable guide to starting a barefoot habit, with safety tips and a 14-day tracker.") + f"""
<section class="wrap free"><div class="index-head"><div><p class="kicker"><a href="/">Free from The Emotional Support Line</a></p><h1>The Earthing Starter Checklist</h1>
<p class="lede">A simple, no-hype plan for spending a few minutes a day with your bare feet on the earth. Print it, stick it on the fridge and tick off the days.</p></div>
<img class="sticker hero-owl" src="/assets/owls/earthing.webp" alt="" width="200" height="200"></div>
<div class="tools"><button class="btn btn-sun" onclick="window.print()">Print or save as PDF</button>{link("what-is-earthing", "What is earthing?")}</div>
<h2>Before you start</h2>
<ul class="check"><li>Find a natural surface near you: grass, soil, sand or smooth stone</li><li>Check it for glass, thorns, sharp sticks and animal mess</li><li>Skip lawns that were recently sprayed with chemicals</li><li>If you have diabetes, poor circulation or foot problems, ask your doctor first</li><li>Leave a pair of slip-on shoes by the door</li></ul>
<h2>The 14-day plan</h2>
<ul class="check"><li><b>Days 1 to 3:</b> two minutes, standing still. Notice the temperature and texture under your feet</li><li><b>Days 4 to 7:</b> five minutes. Walk slowly, or sit with your feet on the ground while you drink your coffee</li><li><b>Days 8 to 14:</b> ten minutes or more. Pair it with something you already do: a phone call, reading, watching the kids play</li><li>Try different surfaces: damp grass, garden soil, sand, a sun-warmed rock</li><li>Wash your feet afterward</li></ul>
<h2>Your 14-day tracker</h2><p class="note">Tick a box each day you get barefoot outside, even for two minutes. Missed a day? Just start again tomorrow.</p>
<div class="tracker">{days}</div>
<h2>Cold-weather options</h2>
<ul class="check"><li>One minute on a patch of lawn on sunny afternoons</li><li>Hands in a pot of garden soil</li><li>Save longer sessions for warmer days, and skip ice entirely</li></ul>
<p class="note">Research on earthing is still early, so we don't make health claims. Many people simply find that a few minutes barefoot outside helps them feel calmer and more present. The Nest app's Earth Charge can time your sessions and keep your streak on your phone.</p>
{SIGNUP}</section>""" + FOOT
(ROOT / "site/free/earthing-checklist.html").write_text(earth)
print("free pages built")

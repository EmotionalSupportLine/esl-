"""Publishes the year's pre-written content on its date.

Runs daily from .github/workflows/publish.yml (and can be run by hand):
    python3 studio/year/publish.py            # publish everything due as of now
    python3 studio/year/publish.py --preview  # build everything, ignoring dates (into /tmp/esl-preview)

Sources (pre-approved by the Editor agent):
    studio/year/blog/<YYYY-MM-DD>-<slug>.md      one blog post, goes live early on its date (Mountain)
    studio/year/forecast/<YYYY-MM-DD>.md         one Energy Forecast, goes live the Saturday before its Sunday

Outputs (into site/):
    blog/<slug>.html, blog/index.html, blog/rss.xml
    forecast/<sunday>.html, forecast/index.html, forecast/rss.xml   <- Mailchimp's RSS campaign reads this
    sitemap.xml

A file with "status: hold" in its front matter is never published.
"""
import datetime, html, json, os, pathlib, re, shutil, sys
from zoneinfo import ZoneInfo
import markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
YEAR = ROOT / "studio" / "year"
SITE = ROOT / "site"
BASE = "https://theemotionalsupportline.com"
MT = ZoneInfo("America/Denver")
PREVIEW = "--preview" in sys.argv
if PREVIEW:
    SITE = pathlib.Path("/tmp/esl-preview")
    if SITE.exists():
        shutil.rmtree(SITE)
    shutil.copytree(ROOT / "site", SITE)
NOW = datetime.datetime.now(MT)

CTA = {
    "call": ("headset-wink", "Need to talk it through?", "Book a 30-minute call with a real, trained supporter. $75, or $50 for Nest members. No sales call first.", "Book a call", "/#calls"),
    "nest": ("sunrise", "Make it a daily habit", "The Nest tracks your morning sun and earthing time, shows the sky for where you are, and includes a monthly group call. NEST_PRICE", "See the Nest", "/#nest"),
    "forecast": ("full-moon", "Get EmoOwl's Energy Forecast", "Every Sunday: the week's moon, sky and one question to sit with. Free.", "Send me the Forecast", "/#forecast"),
    "coaching": ("compass", "Want to go deeper?", "Year of YES! Coaching with Tracee Sioux: two hours a month of one-on-one coaching, guided by your Human Design chart. By application.", "See Year of YES! Coaching", "/year-of-yes"),
    "moon-calendar": ("moon-phases", "Free: the 2027 Moon Calendar", "Every new moon, full moon and eclipse of 2027, in Mountain time, with a reflection question for each. Free to download.", "Get the moon calendar", "/free/moon-calendar-2027"),
    "earthing-checklist": ("earthing", "Free: the Earthing Starter Checklist", "A one-page, printable guide to starting a barefoot habit, with a 14-day tracker. Free to download.", "Get the checklist", "/free/earthing-checklist"),
}
# Tracee's graphics (site/assets/library/) shown in each kind of call-to-action box. See studio/library/LIBRARY.md.
CTA_ART = {"call": "in-the-moment-support", "nest": "nest-come-as-you-are", "forecast": "forecast-cover-owls", "coaching": "year-of-yes-soul-contract"}
CRISIS = "Not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US)."


def parse(path):
    text = path.read_text()
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return meta, body.strip()


def md(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists"])


def owl(name, size, cls="", alt=""):
    return f'<img class="{cls}" src="/assets/owls/{name}.webp" alt="{html.escape(alt)}" width="{size}" height="{size}" loading="lazy">'


def due(date_str, hour=0, days_before=0):
    d = datetime.date.fromisoformat(date_str) - datetime.timedelta(days=days_before)
    return PREVIEW or NOW >= datetime.datetime(d.year, d.month, d.day, hour, tzinfo=MT)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | The Emotional Support Line</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#134f53">
<link rel="canonical" href="{url}">
<link rel="icon" href="/assets/owl-128.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}{ogimg}">
<meta property="og:type" content="article">
<link rel="alternate" type="application/rss+xml" title="The Emotional Support Line blog" href="/blog/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/brand.css">
<link rel="stylesheet" href="/assets/blog.css">
{jsonld}
</head>
<body>
<div class="crisis">Not a crisis line. If you're in danger or thinking about suicide, call or text <a href="tel:988">988</a> (US) or your local emergency number.</div>
<div class="wrap">
  <header class="top">
    <a class="brand" href="/"><img src="/assets/owl-128.png" alt=""><span>The Emotional<br>Support Line</span></a>
    <nav class="links" aria-label="Main">
      <a href="/blog/">Blog</a>
      <a href="/forecast/">Forecast</a>
      <a href="/#nest">The Nest</a>
      <a class="btn btn-sun" href="/#calls">Book a call</a>
    </nav>
  </header>
</div>
<main>
{main}
</main>
<footer><div class="wrap"><span>© {year} The Emotional Support Line</span><span><a href="/blog/">Blog</a> &nbsp; <a href="/forecast/">Forecast archive</a> &nbsp; <a href="/terms.html">Terms</a> &nbsp; <a href="/privacy.html">Privacy</a></span></div></footer>
<script src="/assets/signup.js" defer></script><script src="/assets/crisis-guard.js" defer></script>
</body>
</html>
"""


def page(title, desc, url, main, ogimg="full-moon", jsonld=""):
    ogimg = ogimg if ogimg.startswith("/") else f"/assets/email/{ogimg}.png"
    return PAGE.format(title=html.escape(title), desc=html.escape(desc), url=url, main=main, base=BASE, ogimg=ogimg, jsonld=jsonld, year=NOW.year)


def art(name, cls, alt="", width=480):
    return f'<img class="{cls}" src="/assets/library/{name}.jpg" alt="{html.escape(alt)}" width="{width}" loading="lazy">'


def cta_box(kind, date="2099-01-01", banner=""):
    pose, h, p, btn, href = CTA[kind]
    p = p.replace("NEST_PRICE", "Founding members pay $14 a month for as long as they stay." if date < "2026-12-01" else "$19 a month, or $190 a year.")
    pic = CTA_ART.get(kind)
    img = f'<a href="{href}">{art(pic, "cta-art", h, 220)}</a>' if pic and pic != banner else owl(pose, 120, "sticker")
    return f'<aside class="cta">{img}<div><h2>{h}</h2><p>{p}</p><a class="btn btn-sun" href="{href}">{btn}</a></div></aside>'


def signup():
    return ('<aside class="signup"><img src="/assets/owls/telescope.webp" alt="" width="96" height="96" loading="lazy"><div><h2>EmoOwl\'s Energy Forecast, free every Sunday</h2>'
            '<p>The week\'s moon and sky, a note on getting outside, and one question to sit with.</p>'
            '<form class="field" action="https://traceesioux.us2.list-manage.com/subscribe/post?u=1518241fc7aee7782d17d61e9&amp;id=bd683fce4d" method="post" target="_blank">'
            '<input type="email" name="EMAIL" placeholder="Your email" aria-label="Your email" required><div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_1518241fc7aee7782d17d61e9_bd683fce4d" tabindex="-1" value=""></div><button class="btn btn-sun" type="submit">Send me the Forecast</button></form></div></aside>')


def nice(d):
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")


def rss(title, link, desc, items):
    out = [f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">\n<channel>\n<title>{html.escape(title)}</title>\n<link>{link}</link>\n<description>{html.escape(desc)}</description>\n<language>en-us</language>']
    for it in items:
        out.append(f"<item><title>{html.escape(it['title'])}</title><link>{it['url']}</link><guid isPermaLink=\"true\">{it['url']}</guid>"
                   f"<pubDate>{it['pub'].strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate><description>{html.escape(it['desc'])}</description>"
                   f"<content:encoded><![CDATA[{it['content']}]]></content:encoded></item>")
    out.append("</channel>\n</rss>\n")
    return "\n".join(out)


def absolute(h):
    return h.replace('src="/', f'src="{BASE}/').replace('href="/', f'href="{BASE}/')


def build_blog():
    posts = []
    for f in sorted((YEAR / "blog").glob("*.md")):
        meta, body = parse(f)
        if meta.get("status") == "hold" or not due(meta["date"]):
            continue
        slug = meta["slug"]
        url = f"{BASE}/blog/{slug}"
        content = md(body)
        banner = meta.get("banner", "")
        ogimg = f"/assets/library/{banner}.jpg" if banner else f"/assets/email/{meta['pose']}.png"
        jsonld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": meta["title"], "datePublished": meta["date"], "description": meta["description"], "author": {"@type": "Organization", "name": "The Emotional Support Line"}, "publisher": {"@type": "Organization", "name": "The Emotional Support Line", "logo": {"@type": "ImageObject", "url": BASE + "/assets/icon-512.png"}}, "image": BASE + ogimg, "mainEntityOfPage": url}) + "</script>"
        figure = f'<figure class="banner">{art(banner, "", meta.get("banner_alt", ""))}</figure>' if banner else ""
        main = (f'<article class="wrap post"><header class="post-head"><div><p class="kicker"><a href="/blog/">The Emotional Support Line blog</a> · {nice(meta["date"])}</p>'
                f'<h1>{html.escape(meta["title"])}</h1><p class="lede">{html.escape(meta["description"])}</p></div>{owl(meta["pose"], 220, "sticker hero-owl", "")}</header>'
                f'{figure}<div class="prose">{content}</div>{cta_box(meta["cta"], meta["date"], banner)}{signup()}<p class="safety">{CRISIS} We offer emotional support and coaching, not therapy or medical advice.</p></article>')
        out = SITE / "blog" / f"{slug}.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(meta["title"], meta["description"], url, main, ogimg, jsonld))
        pub = datetime.datetime.fromisoformat(meta["date"] + "T07:00").replace(tzinfo=MT)
        posts.append({"title": meta["title"], "url": url, "slug": slug, "desc": meta["description"], "pose": meta["pose"], "date": meta["date"], "pub": pub,
                      "content": absolute((f'<p><img src="/assets/library/{banner}.jpg" width="480" alt=""></p>' if banner else f'<p><img src="/assets/email/{meta["pose"]}.png" width="160" alt=""></p>') + f'{content}<p><a href="{url}">Read it on the blog</a></p>')})
    posts.sort(key=lambda p: p["date"], reverse=True)
    cards = "".join(f'<a class="card" href="/blog/{p["slug"]}">{owl(p["pose"], 110, "sticker")}<div><span class="date">{nice(p["date"])}</span><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["desc"])}</p></div></a>' for p in posts)
    main = (f'<section class="wrap blog-index"><div class="index-head"><div><h1>The blog</h1><p class="lede">Plain-spoken help for hard weeks, small daily habits, and a little perspective from the sky. A new post every Tuesday.</p></div>'
            f'{owl("reading", 200, "sticker hero-owl")}</div><div class="cards">{cards or "<p>The first post arrives soon.</p>"}</div>{signup()}</section>')
    (SITE / "blog").mkdir(exist_ok=True)
    (SITE / "blog" / "index.html").write_text(page("Blog", "Plain-spoken help for hard weeks, small daily habits, and a little perspective from the sky.", BASE + "/blog/", main, "reading"))
    (SITE / "blog" / "rss.xml").write_text(rss("The Emotional Support Line blog", BASE + "/blog/", "A new post every Tuesday.", posts[:20]))
    return posts


def email_band(sunday):
    """The call + Nest band at the end of each Forecast email. No call push while Tracee is away."""
    away = "2026-11-22" <= sunday <= "2026-12-01"
    cell = lambda img, h, txt, btn, href, bg, fg: (f'<td class="stack" width="50%" valign="top" style="width:50%;padding:0 10px 14px;text-align:center">'
        f'<img src="/assets/email/{img}.png" width="96" alt="" style="display:block;width:96px;height:auto;border:0;margin:0 auto 8px">'
        f'<div style="font-family:Georgia,serif;font-size:18px;font-weight:700;color:#1f1c1c">{h}</div>'
        f'<div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:1.5;color:#524c4f;margin:4px 0 12px">{txt}</div>'
        f'<a href="{href}" style="display:inline-block;background:{bg};color:{fg};text-decoration:none;font-family:Helvetica,Arial,sans-serif;font-weight:800;font-size:15px;padding:12px 22px;border-radius:999px">{btn}</a></td>')
    nest = cell("sunrise", "Join the Nest", "Daily sun, earthing and sky tools, plus the monthly group call.", "See the Nest", "/#nest", "#134f53", "#fcefda")
    second = cell("telescope", "Share the Forecast", "Know someone who'd like a Sunday pause? Send them this.", "Read on the web", "/forecast/", "#d7783a", "#ffffff") if away else \
             cell("headset-wink", "Need to talk it through?", "30 minutes with a real person. $75, or $50 for Nest members.", "Book a call", "/#calls", "#d7783a", "#ffffff")
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fcefda;border-radius:16px;margin:24px 0 8px"><tr><td style="padding:22px 8px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{second}{nest}</tr></table></td></tr></table>'


def group_call_band(sunday):
    """On the first Sunday of the month the Forecast email announces that day's Nest group call."""
    d = datetime.date.fromisoformat(sunday)
    if d.day > 7 or sunday < "2026-12-06":  # the first group call is December 6, 2026
        return ""
    pic = "nest-sundays-11am" if d.month in (11, 12, 1, 2) or (d.month == 3 and d.day < 8) else "nest-first-sundays"  # that graphic says MST
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border:2px solid #fcab79;border-radius:16px;margin:24px 0 8px"><tr>'
            f'<td class="stack" width="190" valign="middle" style="width:190px;padding:16px"><a href="/#nest"><img src="/assets/library/{pic}.jpg" width="170" alt="The Nest group call, first Sunday of every month" style="display:block;width:170px;height:auto;border:0;border-radius:10px"></a></td>'
            f'<td class="stack" valign="middle" style="padding:16px 20px 16px 4px"><div style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:2px;font-weight:800;color:#d7783a;text-transform:uppercase">Today, 11 am Mountain</div>'
            f'<div style="font-family:Georgia,serif;font-size:22px;font-weight:700;color:#134f53;margin:6px 0">The Nest group call</div>'
            f'<div style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;color:#524c4f;margin:0 0 12px">Bring a question, or just listen. Members: the link is in the Calls tab of the Nest app. Not a member yet? The Nest is $19 a month or $190 a year.</div>'
            f'<a href="/#nest" style="display:inline-block;background:#134f53;color:#fcefda;text-decoration:none;font-family:Helvetica,Arial,sans-serif;font-weight:800;font-size:15px;padding:12px 22px;border-radius:999px">See the Nest</a></td></tr></table>')


def build_forecasts():
    items = []
    for f in sorted((YEAR / "forecast").glob("*.md")):
        meta, body = parse(f)
        sunday = meta["date"]
        if meta.get("status") == "hold" or not due(sunday, days_before=1):
            continue
        url = f"{BASE}/forecast/{sunday}"
        content = md(body)
        q = html.escape(meta["question"])
        main = (f'<article class="wrap post"><header class="post-head"><div><p class="kicker"><a href="/forecast/">EmoOwl\'s Energy Forecast</a> · week of {nice(sunday)}</p>'
                f'<h1>{html.escape(meta["subject"])}</h1><p class="lede">{html.escape(meta["preview"])}</p></div>{owl(meta["pose"], 220, "sticker hero-owl")}</header>'
                f'<div class="prose">{content}<div class="question">{owl("journaling", 80, "")}<div><span>A question to sit with</span><p>{q}</p></div></div></div>'
                f'<section class="transit"><h2>Live Human Design transits</h2><p>Where the Sun, Earth, Moon and planets sit in the gates right now. A prompt for reflection, never a prediction.</p><script async src="https://neutrinoplatform.com/js/widget-v2/loader.js"></script><neutrino-widget type="transit" api-key="5a9615047c3d45d235176ff704d765965ff62b14"></neutrino-widget></section>{signup()}<p class="safety">{CRISIS} Sky positions are real astronomy; what they mean for you is a prompt for reflection, never a prediction.</p></article>')
        out = SITE / "forecast" / f"{sunday}.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page(meta["subject"], meta["preview"], url, main, meta["pose"]))
        # The email version: Mailchimp drops this into the template with *|RSSITEM:CONTENT_FULL|*
        email = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td valign="middle" style="padding-right:12px">'
                 f'<h1 style="font-family:Georgia,serif;font-size:28px;line-height:1.2;color:#1f1c1c;margin:0 0 10px">{html.escape(meta["subject"])}</h1>'
                 f'<p style="font-family:Helvetica,Arial,sans-serif;font-size:16px;color:#524c4f;margin:0">{html.escape(meta["preview"])}</p></td>'
                 f'<td width="140" valign="middle"><img src="/assets/email/{meta["pose"]}.png" width="140" alt="" style="display:block;width:140px;height:auto"></td></tr></table>'
                 f'{content.replace("<img ", "<img width=\"320\" style=\"display:block;margin:0 auto;width:320px;max-width:100%;height:auto\" ")}'
                 f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#134f53;border-radius:16px;margin:20px 0"><tr>'
                 f'<td width="80" style="padding:16px 0 16px 16px"><img src="/assets/email/journaling.png" width="64" alt="" style="display:block;width:64px;height:auto"></td>'
                 f'<td style="padding:16px 20px 16px 12px"><div style="font-family:Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:2px;font-weight:800;color:#fcab79;text-transform:uppercase">A question to sit with</div>'
                 f'<div style="font-family:Georgia,serif;font-style:italic;font-size:19px;line-height:1.4;color:#fcefda">{q}</div></td></tr></table>'
                 f'{group_call_band(sunday)}{email_band(sunday)}')
        pub = datetime.datetime.fromisoformat(sunday + "T06:00").replace(tzinfo=MT) - datetime.timedelta(days=1)
        items.append({"title": meta["subject"], "url": url, "desc": meta["preview"], "pub": pub, "sunday": sunday, "pose": meta["pose"], "content": absolute(email)})
    items.sort(key=lambda i: i["sunday"], reverse=True)
    cards = "".join(f'<a class="card" href="/forecast/{i["sunday"]}">{owl(i["pose"], 110, "sticker")}<div><span class="date">Week of {nice(i["sunday"])}</span><h2>{html.escape(i["title"])}</h2><p>{html.escape(i["desc"])}</p></div></a>' for i in items)
    main = (f'<section class="wrap blog-index"><div class="index-head"><div><h1>EmoOwl\'s Energy Forecast</h1><p class="lede">Every Sunday: the week\'s moon and sky, a note on getting outside, and one question to sit with.</p></div>'
            f'{owl("telescope", 200, "sticker hero-owl")}</div><section class="transit"><h2>Live Human Design transits</h2><p>Where the Sun, Earth, Moon and planets sit in the gates right now. A prompt for reflection, never a prediction.</p><script async src="https://neutrinoplatform.com/js/widget-v2/loader.js"></script><neutrino-widget type="transit" api-key="5a9615047c3d45d235176ff704d765965ff62b14"></neutrino-widget></section>{signup()}<div class="cards">{cards}</div></section>')
    (SITE / "forecast").mkdir(exist_ok=True)
    (SITE / "forecast" / "index.html").write_text(page("EmoOwl's Energy Forecast", "The week's moon and sky, every Sunday.", BASE + "/forecast/", main, "telescope"))
    (SITE / "forecast" / "rss.xml").write_text(rss("EmoOwl's Energy Forecast", BASE + "/forecast/", "The week's moon and sky, every Sunday.", items[:8]))
    return items


def sitemap(posts, items):
    urls = [BASE + "/", BASE + "/year-of-yes", BASE + "/blog/", BASE + "/forecast/", BASE + "/free/moon-calendar-2027", BASE + "/free/earthing-checklist", BASE + "/free/100-things"]
    urls += [p["url"] for p in posts] + [i["url"] for i in items]
    body = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    (SITE / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>\n')
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")


def close_founding():
    """From December 1, 2026 the $14 founding offer disappears from the site."""
    cfg = SITE / "assets" / "config.js"
    if NOW.date() >= datetime.date(2026, 12, 1) and not PREVIEW:
        t = cfg.read_text()
        if "foundingOpen: true" in t:
            cfg.write_text(t.replace("foundingOpen: true", "foundingOpen: false"))
            print("Founding price closed on the site.")


if __name__ == "__main__":
    close_founding()
    posts, items = build_blog(), build_forecasts()
    sitemap(posts, items)
    print(f"{NOW:%Y-%m-%d %H:%M} MT: {len(posts)} blog posts and {len(items)} forecasts live" + (" (preview, dates ignored)" if PREVIEW else ""))

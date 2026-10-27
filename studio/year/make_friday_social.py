"""Social posts for blog posts written Oct 26, 2026: each Friday post (on its Friday, 12 pm) and tonight's nine
search pages (spread over the next weeks, 7 pm). Image = the post's library graphic (site/social/library, Instagram-safe).
Writes studio/year/friday-posts.json, picked up by make_search_csv.py."""
import json, pathlib, re, datetime
Y = pathlib.Path(__file__).resolve().parent
SITE = "https://theemotionalsupportline.com"
CR = "Not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US)."
TAGS = "#EmotionalSupportLine #NeedSomeoneToTalkTo #NervousSystemRegulation #PersonalGrowth #FeelHeard"
HOOK = ["New on the blog:", "Fresh read:", "This week on the blog:", "Worth five minutes:", "For your Friday:"]


def meta(f):
    t = f.read_text()
    fm = t.split("---", 2)[1]
    return {k.strip(): v.strip().strip('"') for k, v in (l.split(":", 1) for l in fm.strip().splitlines() if ":" in l)}


posts = []
tonight = sorted(Y.glob("blog/2026-10-26-*.md"))
fridays = sorted(f for f in Y.glob("blog/*.md") if datetime.date.fromisoformat(f.name[:10]).weekday() == 4 and f.name[:10] >= "2026-10-30")
day = datetime.date(2026, 10, 28)
items = []
for f in tonight:
    items.append((f, day.isoformat(), "19:00")); day += datetime.timedelta(days=3)
for f in fridays:
    items.append((f, f.name[:10], "12:00"))
for k, (f, date, time) in enumerate(items):
    m = meta(f)
    url = f"{SITE}/blog/{m['slug']}"
    banner = m.get("banner") or "in-the-moment-support"
    title, desc = m["title"], m["description"]
    invites = m.get("cta") in ("call", "reset", "quiz") or any(w in (title + desc).lower() for w in ("talk", "lonely", "overwhelm", "stress", "calm", "burden", "listen"))
    body = f"{HOOK[k % len(HOOK)]} {title}\n\n{desc}" + ("\n\n" + CR if invites else "")
    tail = f"\n\n{url}" + ("\n\nNot a crisis line. In danger? Call or text 988 (US)." if invites else "")
    bs = f"{title}\n\n{desc}"
    if len(bs) > 295 - len(tail):
        bs = bs[:294 - len(tail)].rsplit(" ", 1)[0] + "…"
    posts.append({"id": f"b-{m['slug']}", "date": date, "time": time, "type": "blog", "link": url,
                  "image": f"{SITE}/social/library/{banner}.jpg",
                  "instagram": f"{body}\n\nRead it: link in bio.\n\n{TAGS}",
                  "facebook": f"{body}\n\n{url}\n\n#EmotionalSupportLine",
                  "linkedin": f"{body}\n\n{url}",
                  "bluesky": bs + tail,
                  "pinterest": {"title": title[:100], "description": desc[:470]}})
(Y / "friday-posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
print(len(posts), "blog posts for social")

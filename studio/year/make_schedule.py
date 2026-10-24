"""Builds studio/year/social-schedule.json: every approved post from today to Oct 31, 2027, with image URLs and
captions for Instagram, Facebook and Pinterest. The weekly Editor task queues each week's posts to Buffer from this file."""
import json, pathlib, datetime, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; Y = ROOT / "studio" / "year"
BASE = "https://theemotionalsupportline.com/social/"
imgs = {p.stem for p in (ROOT / "site" / "social").glob("*.jpg")}
posts = json.loads((ROOT / "studio" / "posts-through-jan.json").read_text()) + json.loads((Y / "social-2027.json").read_text())
LINK = {"call": "https://theemotionalsupportline.com/#calls", "nest": "https://theemotionalsupportline.com/#nest", "forecast": "https://theemotionalsupportline.com/forecast/", "coach": "https://theemotionalsupportline.com/year-of-yes", "blog": "https://theemotionalsupportline.com/blog/"}
out, missing = [], []
for p in sorted(posts, key=lambda p: (p["date"], p.get("time", "08:00"))):
    if p["date"] < "2026-10-25": continue
    files = sorted([s for s in imgs if s == p["id"] or s.startswith(p["id"] + "-")], key=lambda s: (len(s), s))
    if not files: missing.append(p["id"]); continue
    cap = p["caption"]
    text = " ".join(str(p.get(k, "")) for k in ("title", "text", "sub", "body", "button", "myth", "truth", "foot")) + " " + " ".join(str(sl.get("title", "")) + " " + str(sl.get("body", "")) for sl in p.get("slides", []))
    low = (cap + " " + text).lower()
    # where the post sends people, most specific first
    if "moon calendar" in low: link = "https://theemotionalsupportline.com/free/moon-calendar-2027"
    elif "earthing starter checklist" in low: link = "https://theemotionalsupportline.com/free/earthing-checklist"
    elif "new on the blog" in low or "on the blog" in low:
        d0 = datetime.date.fromisoformat(p["date"]); slug = None
        for k in range(0, 4):
            m = list((Y / "blog").glob(f"{(d0 - datetime.timedelta(days=k)).isoformat()}-*.md"))
            if m: slug = m[0].stem[11:]; break
        link = f"https://theemotionalsupportline.com/blog/{slug}" if slug else LINK["blog"]
    elif "free chart" in low or "your type" in low or "which are you" in low: link = "https://theemotionalsupportline.com/#chart"
    elif p["type"] == "forecast": link = LINK["forecast"]
    elif "pay it forward" in low or "gift a call" in low or "gift them" in low: link = "https://theemotionalsupportline.com/#prices"
    elif "book a call" in low or "book a 30" in low or "a support call" in low or "calls are" in low or "calls run" in low or "call with" in low or "a call away" in low: link = LINK["call"]
    elif "year of yes" in low: link = LINK["coach"]
    elif "nest" in low: link = LINK["nest"]
    elif "forecast" in low: link = LINK["forecast"]
    else: link = LINK["call"]
    # safety: anything inviting a call or a talk carries the full 988 line
    CR = "Not a crisis line. If you're in danger or thinking about suicide, call or text 988 (US)."
    invites = link == LINK["call"] or link.endswith("#prices") or any(w in low for w in ("book a call", "talk to", "talk it", "we're here to listen", "a call away", "listen without", "just listen"))
    if invites and "988" not in cap:
        cap = cap.rstrip() + "\n\n" + CR
    tags = p.get("tags", "#EmotionalSupportLine")
    fb = p.get("facebookTags") or " ".join(tags.split()[:2] + (["#EmotionalSupportLine"] if "#EmotionalSupportLine" not in tags.split()[:2] else tags.split()[2:3]))
    if p["type"] == "carousel":
        head = (p.get("slides") or [{}])[0].get("title") or "Save this"
    else:
        head = p.get("pinterestTitle") or p.get("title") or p.get("text") or p.get("myth") or "The Owl's Forecast"
        if p["type"] == "forecast": head = p.get("pinterestTitle") or "The Owl's Forecast: this week's moon and sky"
    fbcap = re.sub(r"[Ll]ink in bio", link, cap)
    pin = cap
    for a, b in (("at the link in bio", "at theemotionalsupportline.com"), ("from the link in bio", "at theemotionalsupportline.com"), ("Link in bio.", "theemotionalsupportline.com"), ("link in bio", "theemotionalsupportline.com")):
        pin = pin.replace(a, b)
    pin = re.sub(r"  +", " ", pin)
    out.append({"id": p["id"], "date": p["date"], "time": p.get("time", "08:00"), "type": p["type"], "status": p.get("status", "approved"),
                "images": [BASE + f + ".jpg" for f in files], "link": link,
                "instagram": f"{cap}\n\n{tags}", "facebook": f"{fbcap}\n\n{fb}",
                "pinterest": {"title": head[:100], "description": pin.strip()[:480]}})
(Y / "social-schedule.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "scheduled posts;", "missing images:", missing)

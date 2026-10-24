"""Builds studio/year/social-schedule.json: every approved post from today to Oct 31, 2027, with image URLs and
captions for Instagram, Facebook and Pinterest. The weekly Editor task queues each week's posts to Buffer from this file."""
import json, pathlib, datetime
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
    cap = p["caption"]; low = cap.lower() + " " + json.dumps(p).lower()
    link = LINK["blog"] if "new on the blog" in low or "blog:" in low else LINK["forecast"] if p["type"] == "forecast" or "forecast" in low else LINK["coach"] if "year of yes" in low else LINK["nest"] if "nest" in low else LINK["call"]
    tags = p.get("tags", "#EmotionalSupportLine")
    fb = p.get("facebookTags") or " ".join(tags.split()[:2] + (["#EmotionalSupportLine"] if "#EmotionalSupportLine" not in tags.split()[:2] else tags.split()[2:3]))
    head = p.get("pinterestTitle") or p.get("title") or p.get("text") or p.get("myth") or "The Owl's Forecast"
    out.append({"id": p["id"], "date": p["date"], "time": p.get("time", "08:00"), "type": p["type"], "status": "approved",
                "images": [BASE + f + ".jpg" for f in files], "link": link,
                "instagram": f"{cap}\n\n{tags}", "facebook": f"{cap}\n\n{fb}",
                "pinterest": {"title": head[:100], "description": cap.replace("Link in bio.", "").replace("link in bio", "theemotionalsupportline.com").strip()[:480]}})
(Y / "social-schedule.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(out), "scheduled posts;", "missing images:", missing)

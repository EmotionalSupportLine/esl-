"""Builds studio/year/social-2027.json (Feb 1 to Oct 31, 2027) in the same format as posts-through-jan.json,
including Sunday Forecast posts, Facebook hashtags and Pinterest titles."""
import json, pathlib, datetime, re, os
ROOT = pathlib.Path(__file__).resolve().parents[2]; Y = ROOT / "studio" / "year"
src = json.loads((Y / "social-src.json").read_text())
fc = {c["w"]: c for c in json.loads((Y / "forecast-copy.json").read_text())}
sky = {w["sunday"]: w for w in json.loads((ROOT / "studio" / "sky-2027.json").read_text())}
ALLOWED = set("🌿💛🧡💙🌕🦉")
posts = []
for date, typ, fields, cap, tags, pose in src:
    d = datetime.date.fromisoformat(date)
    p = {"id": f"{date}-{d.strftime('%a').lower()}-{typ}", "date": date, "time": "08:00", "type": typ, **fields, "caption": cap, "tags": tags, "pose": pose}
    posts.append(p)
for sunday, w in sky.items():
    if sunday < "2027-02-07": continue
    c = fc[w["week"]]
    end = (datetime.date.fromisoformat(sunday) + datetime.timedelta(days=6))
    posts.append({"id": f"{sunday}-sun-forecast", "date": sunday, "time": "09:00", "type": "forecast", "start": sunday, "prompt": c["question"],
                  "caption": f"The Owl's Forecast for {datetime.date.fromisoformat(sunday):%b %-d} to {end:%b %-d}. 🦉\n\n{c['preview']}\n\nThe week's moon and sky, this week's Human Design gates, plus one question to sit with. Get it free every Sunday: link in bio.",
                  "tags": "#OwlsForecast #MoonPhase #AstroWeather #HumanDesign #WeeklyForecast #EmotionalSupportLine", "pose": c["pose"]})
posts.sort(key=lambda p: (p["date"], p["time"]))
problems = []
for p in posts:
    p["facebookTags"] = " ".join(p["tags"].split()[:2] + ["#EmotionalSupportLine"]) if "#EmotionalSupportLine" not in p["tags"].split()[:2] else " ".join(p["tags"].split()[:3])
    head = p.get("title") or p.get("text") or p.get("myth") or (p.get("slides") or [{}])[0].get("title") or "The Owl's Forecast: this week's moon and sky"
    p["pinterestTitle"] = (head if len(head) <= 95 else head[:92] + "...")
    emo = [ch for ch in p["caption"] if ord(ch) > 0x2600 and not ch.isalnum()]
    if len([e for e in emo if e in ALLOWED]) > 1 or any(e not in ALLOWED for e in emo if ord(e) > 0x1F000): problems.append((p["id"], "emoji", emo))
    n = len(p["tags"].split())
    if not (5 <= n <= 8) or "#EmotionalSupportLine" not in p["tags"]: problems.append((p["id"], "tags", n))
    if not os.path.exists(ROOT / "studio" / "poses" / f'{p["pose"]}.png'): problems.append((p["id"], "pose", p["pose"]))
    if p["type"] == "cta" and p.get("button") == "Book a call" and "988" not in p["caption"]: problems.append((p["id"], "988 missing"))
(Y / "social-2027.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
print(len(posts), "posts;", sum(p["type"] == "forecast" for p in posts), "forecast posts"); print("problems:", problems)

# ---- exact sky facts for the Forecast cards (replaces the card's own approximate calculation) ----
import sys
sys.path.insert(0, str(Y))
def week_card(sunday):
    w = sky.get(sunday)
    if not w: return None
    yr = int(sunday[:4]); out = []
    pri = lambda t: 0 if ("moon in" in t or "eclipse" in t) else 1 if "turns" in t else 3 if ("meteor" in t or ":" in t) else 2
    for e in sorted(w["events"], key=lambda e: pri(e["text"])):
        if e["text"].startswith(("Winter solstice", "Spring equinox", "Summer solstice", "Autumn equinox")): continue
        parts = e["when"].split(", ")
        md = datetime.datetime.strptime(f"{parts[1]} {yr if not (sunday[5:7]=='12' and parts[1].startswith('Jan')) else yr+1}", "%b %d %Y")
        text = e["text"].split(" (")[0] if "eclipse" not in e["text"] else e["text"].split(" (")[0]
        text = text.replace("Full moon in", "Full moon in").replace("Penumbral lunar eclipse", "Lunar eclipse")
        out.append({"date": md.strftime("%Y-%m-%dT12:00:00"), "text": text})
        if len(out) == 3: break
    out.sort(key=lambda x: x["date"])
    if not out:
        out = [{"date": None, "text": ("Retrograde: " + ", ".join(r.split(" in ")[0] for r in w["retrogradesInEffect"])) if w["retrogradesInEffect"] else "A quiet week in the sky"}]
    from make_forecasts import phase_name
    return out, f'{phase_name(sunday)}, Moon in {w["moonOnSunday"].split("Moon in ")[1]}'

for p in posts:
    if p["type"] == "forecast":
        r = week_card(p["start"])
        if r: p["events"], p["phase"] = r
(Y / "social-2027.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
jan = json.loads((ROOT / "studio" / "posts-through-jan.json").read_text()); fixed = 0
for p in jan:
    if p["type"] == "forecast":
        r = week_card(p["start"])
        if r: p["events"], p["phase"] = r; fixed += 1
(ROOT / "studio" / "posts-through-jan.json").write_text(json.dumps(jan, indent=1, ensure_ascii=False))
print("exact sky facts added; Nov-Jan forecast cards fixed:", fixed)

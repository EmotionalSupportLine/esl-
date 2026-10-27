"""Buffer bulk-upload CSVs for the search-plan posts (search-posts.json) and the Friday blog posts.
Writes studio/year/buffer-csv/search-<channel>-partN.csv, 100 rows per file (Buffer's limit per upload).
Run after search-posts.py and make_friday_social.py."""
import csv, json, pathlib
Y = pathlib.Path(__file__).resolve().parent
OUT = Y / "buffer-csv"
posts = json.loads((Y / "search-posts.json").read_text())
f = Y / "friday-posts.json"
if f.exists():
    posts += json.loads(f.read_text())
posts.sort(key=lambda p: (p["date"], p["time"]))
rows = {c: [] for c in ("instagram", "facebook", "linkedin", "bluesky", "pinterest")}
for p in posts:
    when = f'{p["date"]} {p["time"]}'
    img = p["image"]
    rows["instagram"].append({"Text": p["instagram"], "Image URL": img, "Tags": "", "Posting Time": when})
    rows["facebook"].append({"Text": p["facebook"], "Image URL": img, "Tags": "", "Posting Time": when})
    rows["linkedin"].append({"Text": p["linkedin"], "Image URL": img, "Tags": "", "Posting Time": when})
    rows["bluesky"].append({"Text": p["bluesky"], "Image URL": img, "Tags": "", "Posting Time": when})
    rows["pinterest"].append({"Text": p["pinterest"]["description"], "Image URL": img, "Tags": "", "Posting Time": when,
                              "Board Name": "Quick Saves", "Title": p["pinterest"]["title"][:100], "Link": p["link"]})
for old in OUT.glob("search-*.csv"):
    old.unlink()
for ch, r in rows.items():
    for k in range(0, len(r), 100):
        chunk = r[k:k + 100]
        name = OUT / f"search-{ch}-part{k // 100 + 1}-{chunk[0]['Posting Time'][:10]}-to-{chunk[-1]['Posting Time'][:10]}.csv"
        with open(name, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(chunk[0].keys()))
            w.writeheader(); w.writerows(chunk)
print(len(posts), "posts per channel ->", sorted(p.name for p in OUT.glob("search-*.csv")))

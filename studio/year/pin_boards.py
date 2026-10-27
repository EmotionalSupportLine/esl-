"""Puts every Pinterest pin in buffer-csv/*pinterest*.csv on one of Tracee's 5 boards (Oct 26, 2026).
Run after any script that rebuilds the Pinterest CSVs (they default to "Quick Saves")."""
import csv, glob, re, pathlib
B1, B2, B3, B4, B5 = "Need Someone to Talk To", "Nervous System Regulation & Calm", "Feeling Stuck? Get Unstuck", "Human Design & Your Purpose", "Moon Phases & Energy Forecast"
TITLE = [(B5, r'\bmoon|eclipse|solstice|equinox|retrograde|earthing|barefoot|meteor|perseid|energy forecast|\bsky\b'),
         (B2, r'nervous system|regulat|\bcalm|breath|reset|vagus|fight.or.flight|freeze|exhale|wired|five things you can see|name it|feet|laughing together|reach for a human'),
         (B1, r'talk|listen|lonely|alone|someone|support line|therap|heard|burden|best friend|a call|calls|conversation|need to say|say the thing'),
         (B4, r'human design|year of yes|yes!|purpose|soul|\bai\b|job|career|coach|generator|projector|manifestor|reflector|be who you are|conditioned|gifts|come to you for|body says|authority|what do you actually want|next chapter|empty nest|midlife'),
         (B3, r'stuck|procrastinat|productiv|decision|\btime\b|money|get anything done|habit|burnout|to-do|overthink|resolution|focus|busy|overwhelm|say no|quiz|not sure')]
LINK = [(B5, r'/forecast|moon-calendar|earthing'), (B2, r'human-reset|co-regulation|nervous|vagus|fight-or-flight|freeze|calm|stress-relief|regulation'),
        (B1, r'#calls|talk|lonely|listen|emotional-support|burden|vent|stranger|crisis'), (B4, r'#chart|year-of-yes|who-are-you-without|human-design|purpose|coach|what-am-i-doing|life-change|#nest'),
        (B3, r'stuck|unstuck|anything-done|procrastination|decision|time-management|quiz|mindset|productivity|self-improvement|personal-growth|money|financial|100-things')]


def board(r):
    title, link = r.get("Title", "").lower(), r.get("Link", "").lower()
    for b, p in TITLE:
        if re.search(p, title): return b
    for b, p in LINK:
        if re.search(p, link): return b
    return B1


for f in sorted(glob.glob(str(pathlib.Path(__file__).parent / "buffer-csv" / "*pinterest*.csv"))):
    rows = list(csv.DictReader(open(f, encoding="utf-8")))
    for r in rows:
        r["Board Name"] = board(r)
        r["Alt Text"] = ("EmoOwl graphic: " + r.get("Title", "").strip())[:490]
    ORDER = ["Text", "Image URL", "Board Name", "Tags", "Posting Time", "Title", "Alt Text", "Link"]  # Buffer's template order
    with open(f, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=ORDER, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print("pins sorted onto 5 boards")

"""Builds studio/year/forecast/<sunday>.md from sky-2027.json (computed sky facts) + forecast-copy.json (hand-written)."""
import json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[2]
Y = ROOT / "studio" / "year"
sky = {w["week"]: w for w in json.loads((ROOT / "studio" / "sky-2027.json").read_text())}
copy = json.loads((Y / "forecast-copy.json").read_text())
phases = json.loads((Y / "phases.json").read_text())
GATE = {1:"Self-Expression",2:"Direction",3:"Ordering",4:"Formulization",5:"Fixed Rhythms",6:"Friction",7:"The Role of the Self",8:"Contribution",9:"Focus",10:"Behavior of the Self",11:"Ideas",12:"Caution",13:"The Listener",14:"Power Skills",15:"Extremes",16:"Skills",17:"Opinions",18:"Correction",19:"Wanting",20:"The Now",21:"The Hunter",22:"Openness",23:"Assimilation",24:"Rationalization",25:"The Spirit of the Self",26:"The Egoist",27:"Caring",28:"The Game Player",29:"Perseverance",30:"Recognition of Feelings",31:"Influence",32:"Continuity",33:"Privacy",34:"Power",35:"Change",36:"Crisis",37:"Friendship",38:"The Fighter",39:"Provocation",40:"Aloneness",41:"Contraction",42:"Growth",43:"Insight",44:"Alertness",45:"The Gatherer",46:"Determination of the Self",47:"Realization",48:"Depth",49:"Principles",50:"Values",51:"Shock",52:"Stillness",53:"Beginnings",54:"Ambition",55:"Spirit",56:"Stimulation",57:"Intuitive Clarity",58:"Vitality",59:"Dispersion",60:"Acceptance",61:"Mystery",62:"Details",63:"Doubt",64:"Confusion"}
SYN = 29.530588853
def phase_name(sunday):
    t = datetime.datetime.fromisoformat(sunday + "T16:00:00+00:00")
    news = [datetime.datetime.fromisoformat(p["t"]) for p in phases if p["kind"] == "new"]
    prev = max(n for n in news if n <= t); age = (t - prev).total_seconds() / 86400
    for lo, hi, name in [(0, 1, "New moon"), (1, 6.4, "Waxing crescent"), (6.4, 8.4, "First quarter"), (8.4, 13.8, "Waxing gibbous"), (13.8, 15.8, "Full moon"),
                         (15.8, 21.1, "Waning gibbous"), (21.1, 23.1, "Last quarter"), (23.1, 28.5, "Waning crescent"), (28.5, 30, "New moon")]:
        if lo <= age < hi: return name
INVITE = {
    "call": "If something is weighing on you this week, a 30-minute support call with a real person is there for you, Mondays and Tuesdays. [Book a call](/#calls)",
    "nest": "The Nest app shows the moon, the planets and your sunrise and sunset every day, and keeps your morning sun and earthing streak going. [See the Nest](/#nest)",
    "chart": "Curious which gates are defined in your own chart? [See your free Human Design chart](/#chart)",
}
n = 0
(Y / "forecast").mkdir(exist_ok=True)
for c in copy:
    w = sky[c["w"]]; hd = w["hd"]
    moon_line = f'{phase_name(w["sunday"])} on Sunday, with the Moon in {w["moonOnSunday"].split("Moon in ")[1]}.'
    ev = "\n".join(f'- **{e["when"]}:** {e["text"]}' for e in w["events"]) or "- A quiet week, with no major shifts in the sky."
    retro = ", ".join(w["retrogradesInEffect"]) if w["retrogradesInEffect"] else "none"
    changes = "".join(f' On {ch["when"]}, the Sun moves into Gate {ch["sunGate"]} ({GATE[ch["sunGate"]]}) and the Earth into Gate {ch["earthGate"]} ({GATE[ch["earthGate"]]}).' for ch in hd["changes"])
    invite = INVITE["nest"] if c["w"] == 4 else [INVITE["call"], INVITE["nest"], INVITE["chart"]][c["w"] % 3]
    body = f"""{c["intro"]}

## The moon this week

{moon_line}

## In the sky this week

{ev}

Retrograde this week: {retro}.

## This week's Human Design gates

![This week's Human Design gate wheel, with the Sun and Earth gates lit](/assets/hd/{w["sunday"]}.png)

The Sun begins the week in **Gate {hd["sunGate"]}, {GATE[hd["sunGate"]]}** (line {hd["sunLine"]}), and the Earth sits opposite in **Gate {hd["earthGate"]}, {GATE[hd["earthGate"]]}**.{changes} Everyone feels the Sun's gate in the background this week, whether or not it's in their own chart. Treat it as a theme to notice, not a forecast.

## Get outside

{c["outside"]}

{invite}
"""
    fm = f'---\ndate: {w["sunday"]}\nsubject: "{c["subject"]}"\npreview: "{c["preview"]}"\npose: {c["pose"]}\nquestion: "{c["question"]}"\nstatus: approved\n---\n'
    (Y / "forecast" / f'{w["sunday"]}.md').write_text(fm + body)
    n += 1
print(n, "forecasts")

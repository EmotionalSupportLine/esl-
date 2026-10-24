"""Draws the weekly Human Design gate wheel: 64 gates around the zodiac, this week's
Sun gate lit in orange and Earth gate lit in teal. Output: site/assets/hd/<sunday>.png (email) + .webp (site)."""
import json, math, pathlib, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gates import ORDER, START

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "site" / "assets" / "hd"; OUT.mkdir(parents=True, exist_ok=True)
F = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
S = 1200  # draw at 2x, save at 600
CREAM, NIGHT, NIGHT2, ORANGE, SUN, TEAL, TEALL, INK = (252,239,218), (19,79,83), (13,58,61), (215,120,58), (252,171,121), (44,166,171), (125,194,197), (31,28,28)
SIGNS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]

def pt(r, lon):
    # Aries at the left (9 o'clock), signs run counter-clockwise like a chart wheel
    a = math.radians(180 - lon)
    return (S/2 + r*math.cos(a), S/2 - r*math.sin(a))

def wedge(d, r0, r1, lon0, lon1, fill):
    pts = [pt(r1, lon0 + (lon1-lon0)*k/12) for k in range(13)] + [pt(r0, lon1 - (lon1-lon0)*k/12) for k in range(13)]
    d.polygon(pts, fill=fill)

def draw(sun_gate, earth_gate, path):
    im = Image.new("RGBA", (S, S), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.ellipse([20,20,S-20,S-20], fill=NIGHT2)
    f_g = ImageFont.truetype(F, 30); f_big = ImageFont.truetype(F, 34)
    for i, g in enumerate(ORDER):
        lon0 = START + i*5.625; lon1 = lon0 + 5.625
        lit = ORANGE if g == sun_gate else TEAL if g == earth_gate else None
        wedge(d, 360, 560, lon0+0.25, lon1-0.25, lit or (26,98,103) if i % 2 else lit or (22,88,93))
        c = pt(470, lon0 + 2.8125)
        d.text(c, str(g), font=f_big if lit else f_g, fill=(255,255,255) if lit else (214,234,233), anchor="mm")
    NAMES = ["ARIES","TAURUS","GEMINI","CANCER","LEO","VIRGO","LIBRA","SCORPIO","SAGITT.","CAPRIC.","AQUARIUS","PISCES"]
    fz = ImageFont.truetype(F, 20)
    for k in range(12):  # zodiac ring
        wedge(d, 290, 352, k*30+0.4, k*30+29.6, (31,110,115))
        d.text(pt(321, k*30+15), NAMES[k], font=fz, fill=(190,225,224), anchor="mm")
    d.ellipse([S/2-285, S/2-285, S/2+285, S/2+285], fill=CREAM)
    # lit beams into the centre
    for g, col in ((sun_gate, ORANGE), (earth_gate, TEAL)):
        mid = START + ORDER.index(g)*5.625 + 2.8125
        x, y = pt(250, mid); d.ellipse([x-26, y-26, x+26, y+26], fill=col)
        pass
    owl = Image.open(ROOT / "studio" / "poses" / "sun-and-moon.png").convert("RGBA"); owl.thumbnail((300, 300))
    im.alpha_composite(owl, (int(S/2 - owl.width/2), int(S/2 - owl.height/2) - 20))
    fl = ImageFont.truetype(F, 30)
    d.text((S/2, S/2 + 160), f"SUN {sun_gate}  ·  EARTH {earth_gate}", font=fl, fill=NIGHT2, anchor="mm")
    im = im.resize((600, 600), Image.LANCZOS)
    im.save(path.with_suffix(".png"), optimize=True)
    im.save(path.with_suffix(".webp"), "WEBP", quality=85)

if __name__ == "__main__":
    weeks = json.loads((ROOT / "studio" / "sky-2027.json").read_text())
    for w in weeks:
        draw(w["hd"]["sunGate"], w["hd"]["earthGate"], OUT / w["sunday"])
    print(len(weeks), "wheels")

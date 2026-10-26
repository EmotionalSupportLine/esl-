"""Builds the rebranded Year of YES! course workbooks for the Nest library.

    python3 studio/workbooks/build.py            # all workbooks -> site/assets/workbooks/*.pdf

Sources:
  src/<name>.md          Tracee's workbook text (cleaned from the 2014-2015 PDFs), with a few markers:
                         [question] text   a question with writing lines under it
                         [assignment] text  an assignment box
                         [lines N]          N writing lines
                         [calendar Label]   a weekly planning page
                         [letter Salutation|Sign-off]  a letter page
                         [contract]  [freepass]  [hundred]
  originals/soul-conomics-N.pdf   Keynote slide decks, kept as-is with ESL branding over the old logos
  originals/joy-roi*.pdf          spreadsheet worksheets, rebuilt as tables
  art/                   cover art cut from Tracee's graphics
"""
import asyncio, base64, html, io, pathlib, re, sys
import markdown, pdfplumber
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "site" / "assets" / "workbooks"
OUT.mkdir(parents=True, exist_ok=True)
FONTS = HERE / "fonts"
LORA = "/usr/share/fonts/truetype/google-fonts/"


def data_uri(path, mime=None):
    p = pathlib.Path(path)
    mime = mime or {"jpg": "image/jpeg", "png": "image/png", "ttf": "font/ttf"}[p.suffix[1:]]
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


CSS = f"""
@font-face {{ font-family: Lora; src: url('{data_uri(LORA + 'Lora-Variable.ttf')}'); font-weight: 400 700; }}
@font-face {{ font-family: Lora; src: url('{data_uri(LORA + 'Lora-Italic-Variable.ttf')}'); font-style: italic; font-weight: 400 700; }}
@font-face {{ font-family: Nunito; src: url('{data_uri(FONTS / 'Nunito.ttf')}'); font-weight: 200 1000; }}
@font-face {{ font-family: Nunito; src: url('{data_uri(FONTS / 'Nunito-Italic.ttf')}'); font-style: italic; font-weight: 200 1000; }}
@font-face {{ font-family: Caveat; src: url('{data_uri(FONTS / 'Caveat.ttf')}'); font-weight: 400 700; }}
:root {{ --teal:#2CA6AB; --night:#134F53; --orange:#D7783A; --sun:#FCAB79; --cream:#FCEFDA; --ink:#1F1C1C; --ink2:#524C4F; }}
@page {{ size: Letter; margin: 0.8in 0.85in 0.85in; }}
@page cover {{ margin: 0; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font: 400 11.2pt/1.6 Nunito, sans-serif; color: var(--ink); }}
.cover {{ page: cover; break-after: page; width: 8.5in; height: 11in; position: relative; overflow: hidden; background: var(--cream); }}
h2 {{ font: 700 22pt/1.15 Lora, serif; color: var(--night); margin: 0 0 12pt; padding-top: 4pt; break-after: avoid; }}
h2::after {{ content: ""; display: block; width: 46pt; height: 3pt; background: var(--orange); border-radius: 3pt; margin-top: 8pt; }}
h2.page {{ break-before: page; }}
h3 {{ font: 700 13.5pt/1.3 Lora, serif; color: var(--orange); margin: 16pt 0 6pt; break-after: avoid; }}
p {{ margin: 0 0 9pt; }}
ul, ol {{ margin: 0 0 10pt; padding-left: 18pt; }}
li {{ margin: 0 0 5pt; }}
ul:has(> li:nth-child(15)) {{ columns: 2; column-gap: 22pt; }}
ul:has(> li:nth-child(15)) li {{ break-inside: avoid; }}
li::marker {{ color: var(--orange); font-weight: 800; }}
strong {{ font-weight: 800; color: var(--night); }}
blockquote {{ margin: 16pt 0; padding: 14pt 20pt; background: var(--cream); border-left: 5pt solid var(--teal); border-radius: 0 12pt 12pt 0;
  font: italic 600 14pt/1.45 Lora, serif; color: var(--night); break-inside: avoid; }}
blockquote p {{ margin: 0; }}
.q {{ margin: 0 0 14pt; break-inside: avoid; }}
.q p {{ font-weight: 700; color: var(--night); margin-bottom: 2pt; }}
.lines {{ break-inside: avoid; }}
.lines i {{ display: block; height: 26pt; border-bottom: 0.8pt solid #d9c9b0; }}
.assign {{ margin: 14pt 0 10pt; padding: 12pt 16pt 12pt 16pt; border-radius: 12pt; background: var(--night); color: var(--cream); break-inside: avoid; }}
.assign b {{ display: block; font: 800 8.5pt/1 Nunito; letter-spacing: 2pt; text-transform: uppercase; color: var(--sun); margin-bottom: 6pt; }}
.assign p {{ margin: 0; }}
.cal {{ break-before: page; }}
.cal table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
.cal th {{ font: 700 10.5pt Lora; color: var(--cream); background: var(--night); padding: 7pt 2pt; }}
.cal th:first-child {{ width: 46pt; background: transparent; }}
.cal td {{ border: 0.8pt solid #d9c9b0; height: 39pt; font: 600 8pt Nunito; color: var(--ink2); vertical-align: top; padding: 3pt; }}
.letter {{ break-before: page; }}
.letter .sal {{ font: 600 22pt/1 Caveat, cursive; color: var(--night); margin: 6pt 0 4pt; }}
.letter .sign {{ font: 600 17pt/1.25 Caveat, cursive; color: var(--night); text-align: right; margin-top: 10pt; }}
.contract {{ border: 2pt solid var(--teal); border-radius: 16pt; padding: 26pt 30pt; margin-top: 10pt; background: #fffaf2; }}
.contract p {{ font: 500 19pt/1.45 Caveat, cursive; color: var(--ink); }}
.contract .sig {{ margin-top: 28pt; border-bottom: 1pt solid var(--ink2); width: 60%; height: 20pt; }}
.pass {{ margin: 22pt auto 0; width: 88%; border: 3pt dashed var(--teal); border-radius: 18pt; padding: 18pt 26pt 22pt; text-align: center; background: #fffaf2; break-inside: avoid; }}
.pass .x {{ text-align: right; font: italic 600 9pt Nunito; color: var(--teal); }}
.pass .big {{ font: italic 700 46pt/1.1 Lora, serif; color: var(--orange); margin: 6pt 0 10pt; letter-spacing: 1pt; }}
.pass p {{ font: italic 500 10.5pt/1.5 Nunito; color: var(--night); margin: 0; }}
.hundred {{ break-before: page; columns: 2; column-gap: 26pt; }}
.hundred h2 {{ column-span: all; }}
.hundred i {{ display: block; height: 24pt; border-bottom: 0.9pt solid #cdb894; font: normal 800 11pt/32pt Nunito; color: var(--orange); break-inside: avoid; }}
.sigblock {{ margin: 16pt 0 0; }}
.sigblock .n {{ font: 600 26pt/1 Caveat, cursive; color: var(--night); }}
.sigblock .r {{ font: 700 9pt Nunito; letter-spacing: 1.5pt; text-transform: uppercase; color: var(--orange); margin-top: 4pt; }}
.end {{ break-before: page; }}
.end .card {{ border-radius: 16pt; padding: 18pt 20pt; margin: 0 0 14pt; background: var(--cream); display: flex; gap: 16pt; align-items: center; }}
.end .card img {{ width: 64pt; }}
.end .card h3 {{ margin: 0 0 4pt; }}
.end .card p {{ margin: 0; }}
.end .safety {{ margin-top: 22pt; font-size: 9.5pt; color: var(--ink2); border-top: 0.8pt solid #d9c9b0; padding-top: 10pt; }}
"""


def lines(n):
    return '<div class="lines">' + "<i></i>" * int(n) + "</div>"


def expand(md_text):
    out = []
    for line in md_text.splitlines():
        s = line.strip()
        m = re.match(r"\[question\]\s*(.+)", s)
        if m:
            out.append(f'<div class="q"><p>{md_inline(m.group(1))}</p>{lines(3)}</div>'); continue
        m = re.match(r"\[assignment\]\s*(.+)", s)
        if m:
            out.append(f'<div class="assign"><b>Assignment</b><p>{md_inline(m.group(1))}</p></div>'); continue
        m = re.match(r"\[lines (\d+)\]", s)
        if m:
            out.append(lines(m.group(1))); continue
        m = re.match(r"\[calendar (.+)\]", s)
        if m:
            days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
            hours = ["6 am", "8 am", "10 am", "Noon", "2 pm", "4 pm", "6 pm", "8 pm", "10 pm"] + [""] * 6
            rows = "".join("<tr><td>" + h + "</td>" + "<td></td>" * 7 + "</tr>" for h in hours[:15])
            out.append(f'<div class="cal"><h2>Your calendar: {html.escape(m.group(1))}</h2><table><tr><th></th>' + "".join(f"<th>{d}</th>" for d in days) + f"</tr>{rows}</table></div>"); continue
        m = re.match(r"\[letter (.+)\|(.+)\]", s)
        if m:
            out.append(f'<div class="sal">{html.escape(m.group(1))}</div>{lines(17)}<div class="sign">{html.escape(m.group(2))}</div>'); continue
        if s == "[contract]":
            out.append('<div class="contract"><p>Dear Soul,</p><p>I commit to hearing whatever you have to say, about whatever issue you want to talk about, for the duration of this workshop.</p>'
                       '<p>In return, my Soul commits to speaking loudly, clearly and persistently, so much so that I cannot mistake or ignore your message.</p><p>Love,</p><div class="sig"></div></div>'); continue
        if s == "[freepass]":
            out.append('<div class="pass"><div class="x">No expiration</div><div class="big">FREE PASS</div><p>Good for releasing all of the unfinished, burdensome “stuff” your Soul says can go. Anything connected to “I really should” or “One day I’m going to” or “I really need to finish that” or “I wish I had time for” or “Why can’t I ever get that done?”</p></div>'); continue
        m = re.match(r"\[signature (.+)\|(.+)\]", s)
        if m:
            out.append(f'<div class="sigblock"><div class="n">{html.escape(m.group(1))}</div><div class="r">{html.escape(m.group(2))}</div></div>'); continue
        if s == "[hundred]":
            out.append('<div class="hundred"><h2>100 Things I Experienced This Year!</h2>' + "".join(f"<i>{n}.</i>" for n in range(1, 101)) + "</div>"); continue
        out.append(line)
    return "\n".join(out)


def md_inline(t):
    return markdown.markdown(t).removeprefix("<p>").removesuffix("</p>")


def owl_img(width):
    return f'<img src="{data_uri(HERE / "art" / "owl.png")}" style="width:{width}" alt="">'


def cover_html(meta):
    art = HERE / "art" / f"{meta['cover']}.jpg"
    band = (f'<div style="position:absolute;left:0;right:0;bottom:0;padding:22pt 40pt 26pt;background:var(--night);color:var(--cream);display:flex;align-items:center;gap:16pt">'
            f'{owl_img("52pt")}<div><div style="font:800 9pt Nunito;letter-spacing:2.4pt;text-transform:uppercase;color:var(--sun)">{html.escape(meta["kind"])}</div>'
            f'<div style="font:700 16pt/1.25 Lora;margin-top:3pt">{html.escape(meta["course"])}</div>'
            f'<div style="font:600 9.5pt Nunito;opacity:.85;margin-top:3pt">{"Free from The Emotional Support Line · theemotionalsupportline.com" if meta.get("end") == "free" else "The Emotional Support Line · Included with the Nest"}</div></div></div>')
    if meta["cover"] in ("time-joygasm-garden",):  # the graphic already carries the title
        return f'<section class="cover"><img src="{data_uri(art)}" style="position:absolute;left:0;top:0;width:100%;height:9.3in;object-fit:cover;object-position:top"></section>'.replace("</section>", band + "</section>")
    if meta.get("cover_crop") == "left":  # art without its own title: crop the picture, set our own title
        title = (f'<div style="position:absolute;left:0;right:0;top:0;padding:46pt 44pt 0;text-align:center">'
                 f'<div style="font:700 54pt/1 Lora;color:var(--night)">{html.escape(meta["title"])}</div>'
                 f'<div style="font:italic 600 16pt/1.35 Lora;color:var(--orange);margin-top:10pt">{html.escape(meta["subtitle"])}</div></div>')
        return (f'<section class="cover"><img src="{data_uri(art)}" style="position:absolute;left:0;top:2.35in;width:100%;height:7in;object-fit:cover;object-position:50% 12%">'
                f'{title}{band}</section>')
    # landscape art on top, our title below
    return (f'<section class="cover"><img src="{data_uri(art)}" style="position:absolute;left:0;top:0;width:100%;height:5.7in;object-fit:cover">'
            f'<div style="position:absolute;left:0;right:0;top:5.95in;padding:0 48pt;text-align:center">'
            f'<div style="font:700 40pt/1.05 Lora;color:var(--night)">{html.escape(meta["title"])}</div>'
            f'<div style="font:italic 600 15pt/1.35 Lora;color:var(--orange);margin-top:10pt">{html.escape(meta["subtitle"])}</div></div>{band}</section>')


def end_html(free=False):
    card = lambda h, p: f'<div class="card">{owl_img("64pt")}<div><h3>{h}</h3><p>{p}</p></div></div>'
    if free:
        return ('<section class="end"><h2>Keep going</h2>'
                + card("Go deeper with the Harvest course", "100 Things is one class of Harvest, an eight-class year-end course on reviewing your intentions, letting go and celebrating. It’s included in the Nest, along with the other Year of YES! courses, guided meditations and a monthly group call. theemotionalsupportline.com/#nest")
                + card("Get EmoOwl’s Energy Forecast", "Every Sunday: the week’s moon and sky and one question to sit with. Free. theemotionalsupportline.com/#forecast")
                + card("Talk it through", "Book a 30-minute call with a real, trained supporter. Never AI. $75, or $50 for Nest members. theemotionalsupportline.com")
                + '<p class="safety">Not a crisis line. If you’re in danger or thinking about suicide, call or text 988 (US) or your local emergency number. '
                  'We offer emotional support and coaching, not therapy or medical advice.<br><br>© The Emotional Support Line. Free to use for yourself; please share the link rather than the file.</p></section>')
    return ('<section class="end"><h2>Keep going</h2>'
            + card("Talk it through", "Book a 30-minute call with a real, trained supporter. Never AI. $75, or $50 for Nest members. Mondays and Tuesdays, noon to 7 pm Mountain. theemotionalsupportline.com")
            + card("Come to the group call", "Nest members meet on the first Sunday of every month at 11 am Mountain. Bring a question, or just listen.")
            + card("Go deeper with Tracee", "Year of YES! Coaching with Tracee Sioux: twelve months, two hours a month, guided by your Human Design. By application at theemotionalsupportline.com/year-of-yes")
            + '<p class="safety">Not a crisis line. If you’re in danger or thinking about suicide, call or text 988 (US) or your local emergency number. '
              'We offer emotional support and coaching, not therapy or medical advice.<br><br>'
              'Course content © 2014–2026 Tracee Sioux. Published by The Emotional Support Line for members of the Nest. Please don’t share or resell.</p></section>')


FOOTER = ('<div style="width:100%;font:600 7.5pt Helvetica,Arial,sans-serif;color:#8a7f78;padding:0 0.85in;display:flex;justify-content:space-between">'
          '<span>The Emotional Support Line · {title}</span><span class="pageNumber"></span></div>')


def parse(path):
    t = path.read_text()
    _, fm, body = t.split("---", 2)
    meta = dict(l.split(": ", 1) for l in fm.strip().splitlines())
    return meta, body


async def render(page, body_html, footer_title=None, landscape=False):
    await page.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{'@page{size:Letter landscape} @page cover{size:Letter landscape;margin:0}' if landscape else ''}</style></head><body>{body_html}</body></html>", wait_until="load")
    if footer_title is None:
        return await page.pdf(print_background=True, prefer_css_page_size=True)
    return await page.pdf(print_background=True, prefer_css_page_size=True, display_header_footer=True,
                          header_template="<div></div>", footer_template=FOOTER.format(title=html.escape(footer_title)))


def merge(parts, dst, title):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for b in parts:
        for pg in PdfReader(io.BytesIO(b)).pages:
            w.add_page(pg)
    w.add_metadata({"/Title": title, "/Author": "Tracee Sioux · The Emotional Support Line"})
    with open(dst, "wb") as f:
        w.write(f)


async def text_workbook(page, name):
    meta, body = parse(HERE / "src" / f"{name}.md")
    content = markdown.markdown(expand(body), extensions=["extra", "sane_lists"])
    first = [True]
    def mark(m):  # every section after the first starts on a new page
        if first[0]:
            first[0] = False
            return m.group(0)
        return m.group(0).replace("<h2>", '<h2 class="page">', 1)
    content = re.sub(r"<h2>", lambda m: mark(m), content)
    cover = await render(page, cover_html(meta))
    inner = await render(page, content + end_html(meta.get("end") == "free"), meta["title"] + " workbook")
    merge([cover, inner], OUT / f"{name}.pdf", meta["title"] + " workbook")


async def joy_roi(page):
    rows = {}
    for f in ["joy-roi", "joy-roi-blank"]:
        with pdfplumber.open(HERE / "originals" / f"{f}.pdf") as pdf:
            rows[f] = pdf.pages[0].extract_tables()[0]
    def table(rows, filled):
        out = ['<table class="roi">']
        for r in rows:
            cells = [(c or "").replace("\n", " ").strip() for c in r]
            if not any(cells) and filled:
                continue
            head = cells[0] in ("Project", "Money", "Time", "Energy/Mindshare") or cells[0].startswith(("Is this project", "Joy Factor", "Could I Outsource", "Does it make sense", "What are my next"))
            tot = cells[0].startswith("Total")
            cls = "h" if head else "t" if tot else ""
            if not filled and cells[0] == "Project":
                cells = ["Project"] + [""] * 5 + ["Total"]
            if not filled and tot:
                cells = [cells[0]] + [""] * 6
            out.append(f'<tr class="{cls}">' + "".join(f"<td>{html.escape(c)}</td>" for c in cells) + "</tr>")
        return "".join(out) + "</table>"
    blank_rows = rows["joy-roi-blank"]
    # the blank version has empty task rows under Joy Factor / Outsource and next steps: keep 8 of each for writing
    css = """<style>
      table.roi{width:100%;border-collapse:collapse;table-layout:fixed;font:600 7.6pt/1.25 Nunito}
      table.roi td{border:0.6pt solid #d9c9b0;padding:3pt 4pt;height:15pt;vertical-align:top}
      table.roi td:first-child{width:22%;font-weight:800;color:#134F53}
      table.roi tr.h td{background:#FCEFDA;color:#134F53;font-weight:800}
      table.roi tr.t td{background:#e6f4f4;font-weight:800}
    </style>"""
    meta = {"cover": "tile-joy-roi", "title": "Joy R.O.I.", "subtitle": "Make joy-driven choices about where your time, money and energy go", "kind": "Worksheet",
            "course": "Joy R.O.I., a Year of YES! worksheet with Tracee Sioux"}
    intro = ('<h2>How to use your Joy R.O.I. worksheet</h2>'
             '<p>Joy R.O.I. is your return on investment in joy. Use it to look honestly at the projects that take your time, money and energy, and decide which ones earn their place in your life.</p>'
             '<ol><li><strong>Project:</strong> write up to five projects, jobs or commitments across the top row.</li>'
             '<li><strong>Money:</strong> what does each one bring in, and what does it cost you each month?</li>'
             '<li><strong>Time:</strong> how many hours does it take each month, and how many hours do you want to give it?</li>'
             '<li><strong>Energy/Mindshare:</strong> on a scale of 1 to 10, how much energy does it take now, and how much do you wish it took?</li>'
             '<li><strong>Is it necessary</strong> to your business or your life?</li>'
             '<li><strong>Joy Factor:</strong> list the tasks involved and give each a joy rating from 1 to 10.</li>'
             '<li><strong>Could you outsource or automate</strong> the tasks you don’t enjoy?</li>'
             '<li><strong>Does it make sense to keep doing this,</strong> and what are your next steps?</li></ol>'
             '<p>The next page is a filled-in example from Tracee’s own year. After that is a blank worksheet for you.</p>')
    body = (css + intro
            + '<h2 class="page">Example: a filled-in worksheet</h2>' + table(rows["joy-roi"], True)
            + '<h2 class="page">Your Joy R.O.I. worksheet</h2>' + table(blank_rows, False) + end_html())
    cover = await render(page, cover_landscape(meta), landscape=True)
    inner = await render(page, body, "Joy R.O.I. worksheet", landscape=True)
    merge([cover, inner], OUT / "joy-roi.pdf", "Joy R.O.I. worksheet")


def cover_landscape(meta, w="11in", h="8.5in"):
    art = HERE / "art" / f"{meta['cover']}.jpg"
    return (f'<section class="cover" style="width:{w};height:{h};display:flex;align-items:stretch">'
            f'<div style="width:52%;display:flex;align-items:center;justify-content:center;background:var(--night);padding:36pt">'
            f'<img src="{data_uri(art)}" style="width:100%;border-radius:18pt;box-shadow:0 20pt 40pt -16pt rgba(0,0,0,.6)"></div>'
            f'<div style="flex:1;padding:64pt 44pt 0;position:relative">{owl_img("58pt")}'
            f'<div style="font:800 9pt Nunito;letter-spacing:2.4pt;text-transform:uppercase;color:var(--orange);margin-top:18pt">{html.escape(meta["kind"])}</div>'
            f'<div style="font:700 44pt/1.05 Lora;color:var(--night);margin-top:8pt">{html.escape(meta["title"])}</div>'
            f'<div style="font:italic 600 15pt/1.4 Lora;color:var(--orange);margin-top:12pt">{html.escape(meta["subtitle"])}</div>'
            f'<div style="position:absolute;left:44pt;right:30pt;bottom:44pt;font:600 10pt/1.5 Nunito;color:var(--ink2)">{html.escape(meta["course"])}<br>The Emotional Support Line · Included with the Nest</div></div></section>')


SKIP = {(1, 1), (1, 2)}  # Soul-Conomics class 1: TraceeSioux.com banner slide and the 2014 Soul vs Ego cover


async def soul_conomics(page):
    """Keep Tracee's Keynote slides; new cover slide; cover the old Sioux Ink logo + TraceeSioux.com on each slide."""
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    owl = ImageReader(str(HERE / "art" / "owl.png"))
    for n in range(1, 8):
        src = HERE / "originals" / f"soul-conomics-{n}.pdf"
        # 1. cover slide, rendered at the deck's own size (1024 x 768 pt)
        meta = {"cover": "tile-soul-conomics", "title": "Soul-Conomics", "subtitle": f"Class {n} workbook: make peace with money and become a money magnet",
                "kind": f"Class {n} slides", "course": "Soul-Conomics, a Year of YES! course with Tracee Sioux"}
        await page.set_content(f"<!doctype html><html><head><style>{CSS}@page{{size:1024pt 768pt;margin:0}} @page cover{{size:1024pt 768pt;margin:0}}</style></head><body>{cover_landscape(meta, '1024pt', '768pt')}</body></html>", wait_until="load")
        cover_pdf = await page.pdf(print_background=True, prefer_css_page_size=True)
        r = PdfReader(str(src)); w = PdfWriter()
        w.add_page(PdfReader(io.BytesIO(cover_pdf)).pages[0])
        with pdfplumber.open(src) as pdf:
            for i, pg in enumerate(pdf.pages):
                if i == 0 or (n, i) in SKIP:
                    continue  # old cover slide, old Tracee Sioux banner and old Soul vs Ego cover
                H = float(pg.height)
                marks = [wd for wd in pg.extract_words() if "TraceeSioux" in wd["text"]]
                patches = []
                for mk in marks:
                    # the Sioux Ink logo image sits just above the link text
                    imgs = [im for im in pg.images if im["bottom"] <= mk["top"] + 4 and mk["top"] - im["bottom"] < 40 and im["x1"] > mk["x0"] - 120 and im["x0"] < mk["x1"] + 120]
                    x0 = min([mk["x0"]] + [im["x0"] for im in imgs]) - 6
                    x1 = max([mk["x1"]] + [im["x1"] for im in imgs]) + 6
                    top = min([mk["top"]] + [im["top"] for im in imgs]) - 4
                    bot = mk["bottom"] + 4
                    patches.append((x0, top, x1, bot))
                buf = io.BytesIO()
                c = canvas.Canvas(buf, pagesize=(float(pg.width), H))
                for x0, top, x1, bot in patches:
                    c.setFillColorRGB(1, 1, 1); c.setStrokeColorRGB(1, 1, 1)
                    c.rect(x0, H - bot, x1 - x0, bot - top, fill=1, stroke=0)
                    s = min(bot - top - 18, 46)
                    c.drawImage(owl, x0 + (x1 - x0 - s * 1.07) / 2, H - top - s - 2, width=s * 1.07, height=s, mask="auto")
                    c.setFillColorRGB(0.075, 0.31, 0.325); c.setFont("Helvetica-Bold", 10)
                    c.drawCentredString((x0 + x1) / 2, H - bot + 4, "theemotionalsupportline.com")
                c.save()
                base = r.pages[i]
                if patches:
                    base.merge_page(PdfReader(buf).pages[0])
                w.add_page(base)
        w.add_metadata({"/Title": f"Soul-Conomics Class {n} workbook", "/Author": "Tracee Sioux · The Emotional Support Line"})
        with open(OUT / f"soul-conomics-{n}.pdf", "wb") as f:
            w.write(f)


async def main():
    only = sys.argv[1:]
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        page = await b.new_page()
        for name in ["time-joygasm", "harvest", "soul-vs-ego", "100-things"]:
            if not only or name in only:
                await text_workbook(page, name)
        if not only or "joy-roi" in only:
            await joy_roi(page)
        if not only or "soul-conomics" in only:
            await soul_conomics(page)
        await b.close()
    for p in sorted(OUT.glob("*.pdf")):
        print(p.name, p.stat().st_size // 1024, "KB")


asyncio.run(main())

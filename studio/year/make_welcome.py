"""Turns welcome-series.md into Mailchimp-ready HTML emails in studio/year/welcome/ (same look as the Forecast template)."""
import re, pathlib, markdown, html
ROOT = pathlib.Path(__file__).resolve().parents[2]; Y = ROOT / "studio" / "year"
tpl = (ROOT / "studio" / "email-template.html").read_text()
import sys
name = sys.argv[1] if len(sys.argv) > 1 else "welcome"   # welcome -> welcome-series.md ; hundred -> hundred-series.md
src = (Y / f"{name}-series.md").read_text().split("\n=== ")[1:]
out = Y / name; out.mkdir(exist_ok=True)
BASE = "https://theemotionalsupportline.com"
for part in src:
    num, rest = part.split("\n", 1)
    head, body = rest.split("\n---\n", 1)
    meta = dict(l.split(": ", 1) for l in head.strip().splitlines())
    lines = body.strip().splitlines(); h1 = lines[0].lstrip("# ").strip(); body_md = "\n".join(lines[1:]).strip()
    content = markdown.markdown(body_md, extensions=["extra"]).replace("FNAMETAG", "*|FNAME|*").replace('href="/', f'href="{BASE}/').replace('src="/', f'src="{BASE}/').replace('<img ', '<img width="440" style="display:block;width:440px;max-width:100%;height:auto;margin:6px auto 18px;border:0;border-radius:14px" ')
    page = tpl.replace("<title>*|MC:SUBJECT|*</title>", f"<title>{html.escape(meta['subject'])}</title>")
    page = page.replace("EmoOwl's Energy Forecast &nbsp;·&nbsp; *|DATE:F j|*", "The Emotional Support Line")
    page = re.sub(r'(<td class="stack body"[^>]*mc:edit="headline">).*?(</td>)', lambda m: f'{m.group(1)}\n            <h1>{html.escape(h1)}</h1>\n          {m.group(2)}', page, flags=re.S)
    page = page.replace("assets/email/full-moon.png", f"assets/email/{meta['pose']}.png")
    page = re.sub(r'(<td class="pad body" style="padding:18px 40px 4px" mc:edit="body">).*?(</td></tr>\n\n      <!-- One question)', lambda m: f'{m.group(1)}\n{content}\n      {m.group(2)}', page, flags=re.S)
    page = re.sub(r'\s*<!-- One question to sit with -->.*?</tr>\n\n', '\n\n', page, count=1, flags=re.S)
    page = page.replace('<span style="display:none;max-height:0;overflow:hidden;opacity:0">*|MC_PREVIEW_TEXT|*</span>', f'<span style="display:none;max-height:0;overflow:hidden;opacity:0">{html.escape(meta["preview"])}</span>')
    if meta.get("from") == "tracee":
        page = page.replace('With you,<br><b style="color:#134f53">EmoOwl</b> at The Emotional Support Line', 'Love,<br><b style="color:#134f53">Tracee</b><br><span style="font-size:14px">Tracee Sioux, creator of Year of YES!</span>')
    (out / f"{num.strip()}.html").write_text(page)
    (out / f"{num.strip()}.txt").write_text(f"Delay: {meta['delay']}\nSubject: {meta['subject']}\nPreview: {meta['preview']}\n")
print(sorted(p.name for p in out.iterdir()))

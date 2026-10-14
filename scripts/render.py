#!/usr/bin/env python3
"""Render a poster HTML to PNG and PDF, and audit it for the defects that
usually slip through: content that overflows or gets clipped, fonts that did
not load, broken images, unreadably small text, and horizontal scroll on a
laptop screen.

It works on any HTML file. The audit script is injected into a temporary copy,
so the poster itself never carries it.

Blocks are the elements marked with data-block="name". Mark decorative
elements that are meant to bleed outside their block with data-bleed.

Usage:
  python3 render.py poster.html [--out DIR] [--scale 1] [--no-pdf] [--crops]

Writes poster.png, poster.pdf and audit.json next to the HTML (or in --out).
With --crops (needs Pillow) it also writes one full-resolution crop per block
in crops/ and a 65 % reduction (sweep.png) for the glance test.
Exit code 1 when the audit finds errors.

Needs Chrome, Chromium or Edge. Set BROWSER_BIN to point at one explicitly.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
FALLBACK_FONTS = ("Times", "Helvetica", "Arial", "DejaVu", "Liberation", "Bitstream", "Verdana", ".SF", "Segoe")
GENERIC = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif",
           "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "fangsong", "-apple-system"}

AUDIT_JS = r"""
<script>
(async () => {
  const MIN_TEXT = %(min_text)d;
  const out = { blocks: [], clipped: [], fonts: { failed: [], system: [] }, images: [], tiny: 0,
                tinySamples: [], placeholders: [], fit: null, canvas: null };
  try { await document.fonts.ready; } catch (e) {}
  await new Promise(r => setTimeout(r, 400));
  const describe = el => {
    const cls = (el.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
    const txt = (el.innerText || el.getAttribute('alt') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return el.tagName.toLowerCase() + (cls ? '.' + cls : '') + (txt ? ` "${txt}"` : '');
  };
  const bleeds = el => !!el.closest('[data-bleed]');
  const visible = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  const root = document.querySelector('[data-poster]') || document.body;
  const rr = root.getBoundingClientRect();
  out.canvas = { w: Math.round(rr.width), h: Math.round(rr.height) };
  for (const b of document.querySelectorAll('[data-block]')) {
    const r = b.getBoundingClientRect();
    const over = [];
    for (const el of b.querySelectorAll('*')) {
      if (bleeds(el) || !visible(el)) continue;
      const e = el.getBoundingClientRect();
      if (!e.width || !e.height) continue;
      const dx = Math.max(r.left - e.left, e.right - r.right), dy = Math.max(r.top - e.top, e.bottom - r.bottom);
      if (dx > 2 || dy > 2) over.push({ el: describe(el), dx: Math.round(dx), dy: Math.round(dy) });
    }
    out.blocks.push({ name: b.dataset.block, x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY),
                      w: Math.round(r.width), h: Math.round(r.height), overflow: over.slice(0, 6), overflowCount: over.length });
  }
  for (const el of root.querySelectorAll('*')) {
    if (bleeds(el) || !visible(el) || el.querySelector('[data-bleed]')) continue;
    const cs = getComputedStyle(el);
    const clipsY = /hidden|clip|auto|scroll/.test(cs.overflowY), clipsX = /hidden|clip|auto|scroll/.test(cs.overflowX);
    const dy = el.scrollHeight - el.clientHeight, dx = el.scrollWidth - el.clientWidth;
    if ((clipsY && dy > 2) || (clipsX && dx > 2)) out.clipped.push({ el: describe(el), hidden_px: Math.max(dy, dx) });
  }
  const used = new Set();
  for (const el of root.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const cs = getComputedStyle(el);
    used.add(cs.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, ''));
    const own_text = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ');
    const ph = own_text.match(/\[[^\]\n]{2,80}\]/);
    if (ph && out.placeholders.length < 8) out.placeholders.push(ph[0]);
    if (parseFloat(cs.fontSize) < MIN_TEXT) { out.tiny++; if (out.tinySamples.length < 5) out.tinySamples.push(describe(el) + ' ' + cs.fontSize); }
  }
  const faces = [...document.fonts];
  const generic = new Set(%(generic)s);
  for (const fam of used) {
    if (generic.has(fam.toLowerCase())) continue;
    const mine = faces.filter(f => f.family.replace(/^["']|["']$/g, '') === fam);
    if (!mine.length) out.fonts.system.push(fam);
    else if (!mine.some(f => f.status === 'loaded')) out.fonts.failed.push(fam);
  }
  for (const img of document.images) if (!img.complete || !img.naturalWidth) out.images.push(describe(img));
  out.fit = { scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth };
  const s = document.createElement('script');
  s.type = 'application/json'; s.id = 'poster-audit'; s.textContent = JSON.stringify(out);
  document.body.appendChild(s);
})();
</script>
"""


def find_browser():
    env = os.environ.get("BROWSER_BIN")
    if env:
        return env
    for c in CANDIDATES:
        if os.path.isabs(c) and Path(c).exists():
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    sys.exit("render.py: no Chrome, Chromium or Edge found. Set BROWSER_BIN=/path/to/browser")


def canvas_size(html):
    m = re.search(r'<meta\s+name="poster-size"\s+content="(\d+)x(\d+)"', html)
    return (int(m.group(1)), int(m.group(2))) if m else (2400, 3600)


def chrome(browser, args, timeout=120):
    base = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--no-default-browser-check", "--virtual-time-budget=15000"]
    return subprocess.run(base + args, capture_output=True, text=True, timeout=timeout)


def audit(browser, html_path, html, w, h, min_text):
    js = AUDIT_JS % {"min_text": min_text, "generic": json.dumps(sorted(GENERIC))}
    patched = html.replace("</body>", js + "</body>") if "</body>" in html else html + js
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=html_path.parent, delete=False,
                                     prefix=".audit-", encoding="utf-8") as tmp:
        tmp.write(patched)
    try:
        res = chrome(browser, [f"--window-size={w},{h}", "--dump-dom", Path(tmp.name).as_uri()])
    finally:
        os.unlink(tmp.name)
    m = re.search(r'<script type="application/json" id="poster-audit">(.*?)</script>', res.stdout, re.S)
    if not m:
        sys.exit("render.py: the audit did not finish (page error or timeout). stderr:\n" + res.stderr[-800:])
    return json.loads(m.group(1))


def pdf_checks(pdf):
    notes = []
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        pages = re.search(r"Pages:\s+(\d+)", info)
        if pages and pages.group(1) != "1":
            notes.append(("warning", f"PDF has {pages.group(1)} pages; add @page {{ size: <W>px <H>px; margin: 0 }}"))
    if shutil.which("pdffonts"):
        fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
        names = {re.sub(r"^[A-Z]{6}\+", "", l.split()[0]) for l in fonts.splitlines()[2:] if l.strip()}
        bad = sorted(n for n in names if n.startswith(FALLBACK_FONTS))
        if bad:
            notes.append(("warning", "PDF uses fallback fonts (a web font did not load in time?): " + ", ".join(bad)))
    return notes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out", help="output directory (default: next to the HTML)")
    ap.add_argument("--scale", type=float, default=1, help="device scale factor for the PNG")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--crops", action="store_true", help="write per-block crops and a 65%% sweep (Pillow)")
    ap.add_argument("--min-text", type=int, default=13, help="smallest acceptable text size in px")
    a = ap.parse_args()

    html_path = Path(a.html).resolve()
    html = html_path.read_text(encoding="utf-8")
    out = Path(a.out).resolve() if a.out else html_path.parent
    out.mkdir(parents=True, exist_ok=True)
    stem = html_path.stem
    browser = find_browser()
    w, h = canvas_size(html)

    rep = audit(browser, html_path, html, w, h, a.min_text)
    laptop = audit(browser, html_path, html, 1440, 900, a.min_text)

    png = out / f"{stem}.png"
    chrome(browser, [f"--window-size={w},{h}", f"--force-device-scale-factor={a.scale}",
                     f"--screenshot={png}", html_path.as_uri()])
    issues = []
    if not png.exists():
        issues.append(("error", "PNG was not written"))
    pdf = out / f"{stem}.pdf"
    if not a.no_pdf:
        chrome(browser, ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", html_path.as_uri()])
        issues += pdf_checks(pdf) if pdf.exists() else [("error", "PDF was not written")]

    cw, ch = rep["canvas"]["w"], rep["canvas"]["h"]
    if abs(cw / w - 1) > 0.01 or abs(ch / h - cw / w) > 0.01:
        issues.append(("warning", f"poster measures {cw}x{ch}, canvas is {w}x{h}: "
                       "set <meta name=\"poster-size\"> and give [data-poster] that exact size"))
    if not rep["blocks"]:
        issues.append(("warning", "no [data-block] elements: overflow is only checked per block"))
    for b in rep["blocks"]:
        if b["overflowCount"]:
            worst = ", ".join(f'{o["el"]} (+{max(o["dx"], o["dy"])}px)' for o in b["overflow"][:3])
            issues.append(("error", f'block "{b["name"]}": {b["overflowCount"]} element(s) outside it: {worst}'))
    for c in rep["clipped"][:8]:
        issues.append(("error", f'clipped content: {c["el"]} hides {c["hidden_px"]}px'))
    for f in rep["fonts"]["failed"]:
        issues.append(("error", f"web font did not load: {f}"))
    if rep["fonts"]["system"]:
        issues.append(("warning", "fonts not embedded or linked (will look different on other machines): "
                       + ", ".join(rep["fonts"]["system"])))
    if rep["placeholders"]:
        issues.append(("error", "template placeholders left in the poster: " + ", ".join(rep["placeholders"][:5])))
    for i in rep["images"]:
        issues.append(("error", f"broken image: {i}"))
    if rep["tiny"]:
        issues.append(("warning", f"{rep['tiny']} text element(s) under {a.min_text}px, e.g. "
                       + "; ".join(rep["tinySamples"][:3])))
    if laptop["fit"]["scrollWidth"] > laptop["fit"]["innerWidth"] + 1:
        issues.append(("warning", f"horizontal scroll at 1440px wide ({laptop['fit']['scrollWidth']}px): "
                       "scale the poster to the viewport (see the template's fit script)"))

    if a.crops and png.exists():
        try:
            from PIL import Image
            im = Image.open(png)
            k = im.width / max(rep["canvas"]["w"], 1)  # rects come in the page's own (possibly zoomed) px
            crops = out / "crops"
            crops.mkdir(exist_ok=True)
            for b in rep["blocks"]:
                box = [round(v * k) for v in (b["x"] - 12, b["y"] - 12, b["x"] + b["w"] + 12, b["y"] + b["h"] + 12)]
                safe = re.sub(r"[^\w-]+", "-", b["name"])
                im.crop(box).save(crops / f"{safe}.png")
            im.resize((round(im.width * 0.65), round(im.height * 0.65))).save(out / "sweep.png")
        except ImportError:
            issues.append(("warning", "--crops needs Pillow: pip install pillow"))

    errors = [m for s, m in issues if s == "error"]
    (out / "audit.json").write_text(json.dumps({"canvas": [w, h], "issues": issues, "raw": rep}, indent=2, ensure_ascii=False))
    print(f"PNG  {png}" + (f"\nPDF  {pdf}" if not a.no_pdf and pdf.exists() else ""))
    print(f"canvas {w}x{h} · {len(rep['blocks'])} blocks · {len(errors)} error(s) · {len(issues) - len(errors)} warning(s)")
    for s, m in issues:
        print(f"  {s.upper():7} {m}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

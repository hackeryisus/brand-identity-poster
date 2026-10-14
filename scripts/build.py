#!/usr/bin/env python3
"""Turn a poster source file into one self-contained HTML file.

Placeholders (paths are relative to the source file):

  {{img:path}}            data URI of an image (svg, png, jpg, webp, gif)
  {{img:path?w=1600}}     same, resized to that width and re-encoded as WebP
                          (needs Pillow; ideal for large photos and scenes)
  {{svg:path}}            the SVG markup inlined (so CSS can style it)
  {{mask:path}}           data URI meant for CSS mask-image. Use it to recolor
                          a logo: background: <color>; mask: url({{mask:...}})
                          Works with SVG and with PNG/WebP that have alpha.
  {{font:path}}           data URI of a font file (woff2, woff, ttf, otf) for
                          @font-face, when the brand font is not on Google Fonts
  {{lucide:name}}         inline SVG of a Lucide icon (fetched once from unpkg,
                          pinned version, cached in ~/.cache/brand-identity-poster)

Usage:
  python3 build.py poster.src.html poster.html
"""
import base64, io, mimetypes, re, sys, urllib.request
from pathlib import Path

LUCIDE_VERSION = "0.542.0"
LUCIDE_URL = "https://unpkg.com/lucide-static@{v}/icons/{name}.svg"
CACHE = Path.home() / ".cache" / "brand-identity-poster" / f"lucide-{LUCIDE_VERSION}"

MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif", ".avif": "image/avif",
        ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".otf": "font/otf"}


def fail(msg):
    sys.exit(f"build.py: {msg}")


def data_uri(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def resolve(base, ref):
    path, _, query = ref.partition("?")
    p = (base / path).resolve()
    if not p.exists():
        fail(f"file not found: {path} (looked in {p})")
    opts = dict(kv.split("=", 1) for kv in query.split("&") if "=" in kv)
    return p, opts


def image(base, ref):
    p, opts = resolve(base, ref)
    mime = MIME.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0]
    if not mime:
        fail(f"unknown image type: {p.name}")
    if "w" in opts and p.suffix.lower() != ".svg":
        try:
            from PIL import Image
        except ImportError:
            fail("resizing (?w=) needs Pillow: pip install pillow")
        im = Image.open(p)
        w = int(opts["w"])
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=int(opts.get("q", 80)))
        return data_uri(buf.getvalue(), "image/webp")
    return data_uri(p.read_bytes(), mime)


def inline_svg(base, ref):
    p, _ = resolve(base, ref)
    svg = p.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->", "", svg, flags=re.S).strip()
    if not svg.startswith("<svg"):
        fail(f"{p.name} does not look like an SVG file")
    return svg


def lucide(name):
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"{name}.svg"
    if not cached.exists():
        url = LUCIDE_URL.format(v=LUCIDE_VERSION, name=name)
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                cached.write_bytes(r.read())
        except Exception as e:
            fail(f"could not fetch Lucide icon '{name}' ({url}): {e}. Check the name at lucide.dev/icons")
    svg = re.sub(r"<!--.*?-->", "", cached.read_text(encoding="utf-8"), flags=re.S).strip()
    # Let CSS control size and stroke: drop fixed width/height/stroke-width on the root only.
    root, rest = re.match(r"(<svg\b[^>]*>)(.*)", svg, re.S).groups()
    root = re.sub(r'\s(width|height|stroke-width)="[^"]*"', "", root)
    root = root.replace('class="lucide', 'aria-hidden="true" class="icon lucide', 1)
    return root + rest


def main():
    if len(sys.argv) != 3:
        fail("usage: build.py <source.html> <output.html>")
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    base = src.resolve().parent
    html = src.read_text(encoding="utf-8")
    handlers = {
        "img": lambda r: image(base, r),
        "mask": lambda r: image(base, r),
        "font": lambda r: image(base, r),
        "svg": lambda r: inline_svg(base, r),
        "lucide": lucide,
    }

    def sub(m):
        kind, ref = m.group(1), m.group(2).strip()
        return handlers[kind](ref)

    html = re.sub(r"\{\{(img|mask|font|svg|lucide):([^}]+)\}\}", sub, html)
    left = re.search(r"\{\{[a-z]+:[^}]*\}\}", html)
    if left:
        fail(f"unknown placeholder: {left.group(0)}")
    out.write_text(html, encoding="utf-8")
    print(f"{out} · {len(html.encode()) // 1024} KB")


if __name__ == "__main__":
    main()

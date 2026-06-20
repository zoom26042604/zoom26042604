#!/usr/bin/env python3
"""Genere les banners du README en Catppuccin Mocha Peach avec la police Baldur.
Le texte est converti en traces vectoriels (paths) -> aucune dependance police au rendu.
Usage: python3 tools/gen_banners.py
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "baldur", "Baldur.ttf")
OUT = os.path.join(ROOT, "banners")

# Palette Catppuccin Mocha
C = {
    "base": "#1e1e2e", "mantle": "#181825", "crust": "#11111b",
    "text": "#cdd6f4", "subtext": "#a6adc8", "overlay": "#6c7086",
    "surface0": "#313244", "surface1": "#45475a",
    "peach": "#fab387", "peachdark": "#e8956b",
    "mauve": "#cba6f7", "blue": "#89b4fa",
}

_font = TTFont(FONT)
_glyphs = _font.getGlyphSet()
_cmap = _font.getBestCmap()
_upm = _font["head"].unitsPerEm
_hmtx = _font["hmtx"]
try:
    _cap = _font["OS/2"].sCapHeight or _font["hhea"].ascent
except Exception:
    _cap = _font["hhea"].ascent


def text_path(s):
    """Retourne (d, largeur_en_unites) du texte en unites de police."""
    pen = SVGPathPen(_glyphs)
    x = 0
    for ch in s:
        gname = _cmap.get(ord(ch))
        if gname is None:
            x += int(_upm * 0.35)  # espace de secours
            continue
        _glyphs[gname].draw(TransformPen(pen, (1, 0, 0, 1, x, 0)))
        x += _hmtx[gname][0]
    return pen.getCommands(), x


def title_svg(text, size, color, banner_w, banner_h, x_left=None):
    """Place un titre Baldur, centre verticalement, retourne le markup <path>."""
    d, wunits = text_path(text)
    scale = size / _upm
    tw = wunits * scale
    tx = x_left if x_left is not None else (banner_w - tw) / 2
    ty = banner_h / 2 + (_cap * scale) / 2
    return (f'<path d="{d}" fill="{color}" '
            f'transform="translate({tx:.2f},{ty:.2f}) scale({scale:.5f},{-scale:.5f})"/>'), tw


def section_banner(filename, text):
    w, h = 900, 70
    pad = 30
    stripe_x, stripe_w = 26, 7
    title, _ = title_svg(text, 40, C["peach"], w, h, x_left=stripe_x + stripe_w + 18)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{C['mantle']}" stroke="{C['surface0']}" stroke-width="1.5"/>
  <rect x="{stripe_x}" y="{(h-34)//2}" width="{stripe_w}" height="34" rx="3.5" fill="{C['peach']}"/>
  {title}
  <circle cx="{w-58}" cy="{h//2}" r="3.5" fill="{C['surface1']}"/>
  <circle cx="{w-44}" cy="{h//2}" r="3.5" fill="{C['peach']}" opacity="0.5"/>
  <circle cx="{w-30}" cy="{h//2}" r="3.5" fill="{C['peach']}"/>
</svg>'''
    open(os.path.join(OUT, filename), "w").write(svg)
    print("ok:", filename)


def header_banner():
    w, h = 900, 220
    name, nw = title_svg("Nathan FERRE", 92, C["peach"], w, h)
    # repositionner verticalement (nom en haut, sous-titre dessous)
    d, wunits = text_path("Nathan FERRE")
    scale = 92 / _upm
    tx = (w - wunits * scale) / 2
    ty = 118
    name = (f'<path d="{d}" fill="{C["peach"]}" '
            f'transform="translate({tx:.2f},{ty:.2f}) scale({scale:.5f},{-scale:.5f})"/>')
    sub, sw = text_path("Infrastructure  -  Web Dev  -  Cloud")
    ssc = 30 / _upm
    stx = (w - sw * ssc) / 2
    subtitle = (f'<path d="{d if False else sub}" fill="{C["subtext"]}" '
                f'transform="translate({stx:.2f},162) scale({ssc:.5f},{-ssc:.5f})"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{C['base']}"/>
      <stop offset="100%" stop-color="{C['crust']}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{C['peach']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{C['peach']}"/>
      <stop offset="100%" stop-color="{C['peach']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="{C['surface0']}" stroke-width="1.5"/>
  {name}
  {subtitle}
  <rect x="270" y="186" width="360" height="3" rx="1.5" fill="url(#rule)"/>
</svg>'''
    open(os.path.join(OUT, "header.svg"), "w").write(svg)
    print("ok: header.svg")


def footer_banner():
    w, h = 900, 110
    txt, tw = text_path("thanks for stopping by")
    sc = 26 / _upm
    tx = (w - tw * sc) / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{C['crust']}"/>
      <stop offset="100%" stop-color="{C['base']}"/>
    </linearGradient>
    <linearGradient id="frule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{C['peach']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{C['peach']}"/>
      <stop offset="100%" stop-color="{C['peach']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="20" fill="url(#fg)"/>
  <rect x="200" y="34" width="500" height="2.5" rx="1.25" fill="url(#frule)"/>
  <path d="{txt}" fill="{C['subtext']}" transform="translate({tx:.2f},78) scale({sc:.5f},{-sc:.5f})"/>
</svg>'''
    open(os.path.join(OUT, "footer.svg"), "w").write(svg)
    print("ok: footer.svg")


if __name__ == "__main__":
    header_banner()
    section_banner("about-me.svg", "About Me")
    section_banner("technologies.svg", "Technologies")
    section_banner("projects.svg", "Projects")
    section_banner("stats.svg", "Stats")
    section_banner("contact.svg", "Contact")
    footer_banner()
    print("done")

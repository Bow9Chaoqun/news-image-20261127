#!/usr/bin/env python3
"""Draw the front page for Friday 27 November 2026.

The picture is a broadsheet front page for the make.fun
news-image-20261127 bounty: one lead story, five more stories in
two rows, and a ticker of shorter items along the foot.

Everything is painted with Pillow on a canvas twice the final size
and then downscaled, so the lettering stays crisp at 1024 x 1024.

    python3 build_image.py        # writes ./entry.png

main.py is the graded entry program; it only copies this PNG.
"""

from dataclasses import dataclass
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCALE = 2
SIZE = 1024
CANVAS = SIZE * SCALE
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

PAPER = (247, 243, 232)
CARD = (255, 253, 246)
INK = (22, 26, 43)
NAVY = (27, 42, 74)
BODY_INK = (30, 30, 34)
MUTED = (96, 92, 84)
GOLD = (212, 168, 74)
RUST = (178, 58, 32)
TEAL = (18, 110, 105)
OCHRE = (164, 110, 20)
PLUM = (110, 52, 110)
PINE = (34, 96, 58)
SLATE = (70, 90, 112)

FONTS = Path("/usr/share/fonts/truetype/liberation")
SERIF_BOLD = FONTS / "LiberationSerif-Bold.ttf"
SANS_BOLD = FONTS / "LiberationSans-Bold.ttf"
SANS = FONTS / "LiberationSans-Regular.ttf"
SANS_ITALIC = FONTS / "LiberationSans-Italic.ttf"


def face(path, points):
    return ImageFont.truetype(str(path), points * SCALE)


def fit_lines(draw, text, font, width):
    """Wrap text to the given pixel width, returning a list of lines."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def line_step(font, factor=1.18):
    ascent, descent = font.getmetrics()
    return int((ascent + descent) * factor)


def paint_lines(draw, x, y, lines, font, colour, factor=1.18):
    step = line_step(font, factor)
    for line in lines:
        draw.text((x, y), line, font=font, fill=colour)
        y += step
    return y


def block_height(font, n_lines, factor=1.18):
    return line_step(font, factor) * n_lines // SCALE


def centred_line(draw, y, text, font, colour):
    draw.text((CANVAS // 2, y), text, font=font, fill=colour, anchor="ma")
    ascent, descent = font.getmetrics()
    return y + ascent + descent


def tag_chip(draw, x, y, wording, colour):
    font = face(SANS_BOLD, 19)
    wide = draw.textlength(wording, font=font)
    draw.rounded_rectangle(
        [x, y, x + wide + 24 * SCALE, y + 30 * SCALE],
        radius=7 * SCALE, fill=colour)
    draw.text((x + 12 * SCALE, y + 4 * SCALE), wording, font=font,
              fill=(255, 255, 255))


def burst(draw, cx, cy, radius, colour, points=8):
    pts = []
    for k in range(points * 2):
        angle = -pi / 2 + k * pi / points
        reach = radius if k % 2 == 0 else radius * 0.42
        pts.append((cx + reach * cos(angle), cy + reach * sin(angle)))
    draw.polygon(pts, fill=colour)


# ------------------------------------------------------------- glyphs
def glyph_tower(draw, cx, cy, r):
    w = 6 * SCALE
    base = cy + r * 0.9
    draw.rectangle([cx - r * 0.34, cy - r * 0.75, cx - r * 0.02, base],
                   outline=INK, width=w)
    draw.rectangle([cx + r * 0.08, cy - r * 0.35, cx + r * 0.36, base],
                   outline=INK, width=w)
    for k in range(4):
        yy = cy - r * 0.55 + k * r * 0.32
        draw.line([cx - r * 0.28, yy, cx - r * 0.08, yy], fill=INK, width=w - 2 * SCALE)
    draw.line([cx - r * 0.55, base, cx + r * 0.55, base], fill=INK, width=w)
    burst(draw, cx - r * 0.18, cy - r * 0.85, r * 0.34, RUST)
    draw.arc([cx + r * 0.05, cy - r * 1.05, cx + r * 0.75, cy - r * 0.45],
             200, 340, fill=MUTED, width=4 * SCALE)
    draw.arc([cx + r * 0.2, cy - r * 0.9, cx + r * 0.9, cy - r * 0.3],
             200, 340, fill=MUTED, width=4 * SCALE)


def glyph_scales(draw, cx, cy, r):
    w = 6 * SCALE
    draw.line([cx, cy - r * 0.9, cx, cy + r * 0.85], fill=INK, width=w)
    draw.line([cx - r * 0.85, cy - r * 0.55, cx + r * 0.85, cy - r * 0.55],
              fill=INK, width=w)
    draw.line([cx - r * 0.6, cy + r * 0.85, cx + r * 0.6, cy + r * 0.85],
              fill=INK, width=w)
    for side in (-1, 1):
        px = cx + side * r * 0.85
        draw.line([px, cy - r * 0.55, px, cy - r * 0.05], fill=INK, width=w - 2 * SCALE)
        draw.arc([px - r * 0.34, cy - r * 0.28, px + r * 0.34, cy + r * 0.28],
                 0, 180, fill=TEAL, width=w)
    draw.ellipse([cx - r * 0.1, cy - r * 1.0, cx + r * 0.1, cy - r * 0.8],
                 fill=RUST)


def glyph_rocket(draw, cx, cy, r):
    w = 6 * SCALE
    draw.polygon([(cx, cy - r * 0.95), (cx + r * 0.34, cy - r * 0.1),
                  (cx + r * 0.34, cy + r * 0.45), (cx, cy + r * 0.62),
                  (cx - r * 0.34, cy + r * 0.45), (cx - r * 0.34, cy - r * 0.1)],
                 outline=INK, width=w)
    draw.ellipse([cx - r * 0.16, cy - r * 0.55, cx + r * 0.16, cy - r * 0.23],
                 outline=PLUM, width=w - SCALE)
    draw.polygon([(cx - r * 0.34, cy + r * 0.25), (cx - r * 0.62, cy + r * 0.72),
                  (cx - r * 0.34, cy + r * 0.55)], fill=RUST)
    draw.polygon([(cx + r * 0.34, cy + r * 0.25), (cx + r * 0.62, cy + r * 0.72),
                  (cx + r * 0.34, cy + r * 0.55)], fill=RUST)
    draw.polygon([(cx - r * 0.14, cy + r * 0.62), (cx + r * 0.14, cy + r * 0.62),
                  (cx, cy + r * 1.0)], fill=GOLD)
    burst(draw, cx + r * 0.72, cy - r * 0.8, r * 0.14, GOLD)
    burst(draw, cx - r * 0.78, cy - r * 0.4, r * 0.1, GOLD)


def glyph_helicopter(draw, cx, cy, r):
    w = 6 * SCALE
    draw.rounded_rectangle([cx - r * 0.55, cy - r * 0.3, cx + r * 0.45, cy + r * 0.35],
                           radius=14 * SCALE, outline=INK, width=w)
    draw.ellipse([cx + r * 0.18, cy - r * 0.16, cx + r * 0.42, cy + r * 0.08],
                 outline=SLATE, width=w - 2 * SCALE)
    draw.line([cx + r * 0.45, cy, cx + r * 0.95, cy - r * 0.12], fill=INK, width=w - SCALE)
    draw.line([cx + r * 0.85, cy - r * 0.42, cx + r * 0.85, cy + r * 0.18],
              fill=RUST, width=w - SCALE)
    draw.line([cx - r * 0.05, cy - r * 0.3, cx - r * 0.05, cy - r * 0.62],
              fill=INK, width=w - SCALE)
    draw.line([cx - r * 0.95, cy - r * 0.62, cx + r * 0.95, cy - r * 0.62],
              fill=INK, width=w)
    draw.line([cx - r * 0.45, cy + r * 0.35, cx - r * 0.3, cy + r * 0.62],
              fill=INK, width=w - 2 * SCALE)
    draw.line([cx + r * 0.3, cy + r * 0.35, cx + r * 0.45, cy + r * 0.62],
              fill=INK, width=w - 2 * SCALE)
    draw.line([cx - r * 0.5, cy + r * 0.62, cx + r * 0.5, cy + r * 0.62],
              fill=INK, width=w - 2 * SCALE)


def glyph_boat(draw, cx, cy, r):
    w = 6 * SCALE
    draw.line([cx, cy - r * 0.9, cx, cy + r * 0.25], fill=INK, width=w - SCALE)
    draw.polygon([(cx, cy - r * 0.9), (cx, cy - r * 0.1),
                  (cx + r * 0.5, cy - r * 0.1)], fill=TEAL)
    draw.polygon([(cx - r * 0.15, cy - r * 0.55), (cx - r * 0.15, cy - r * 0.1),
                  (cx - r * 0.55, cy - r * 0.1)], outline=INK, width=w - 2 * SCALE)
    draw.polygon([(cx - r * 0.75, cy + r * 0.25), (cx + r * 0.75, cy + r * 0.25),
                  (cx + r * 0.55, cy + r * 0.6), (cx - r * 0.55, cy + r * 0.6)],
                 outline=INK, width=w)
    for k, yy in enumerate((0.78, 0.95)):
        draw.arc([cx - r * 0.9, cy + r * yy - r * 0.14, cx - r * 0.1, cy + r * yy + r * 0.14],
                 180, 360, fill=SLATE, width=4 * SCALE)
        draw.arc([cx + r * 0.1, cy + r * yy - r * 0.14, cx + r * 0.9, cy + r * yy + r * 0.14],
                 180, 360, fill=SLATE, width=4 * SCALE)


def glyph_retreat(draw, cx, cy, r):
    w = 6 * SCALE
    draw.line([cx + r * 0.45, cy - r * 0.9, cx + r * 0.45, cy + r * 0.85],
              fill=INK, width=w - SCALE)
    draw.polygon([(cx + r * 0.45, cy - r * 0.9), (cx - r * 0.35, cy - r * 0.62),
                  (cx + r * 0.45, cy - r * 0.34)], fill=PINE)
    draw.arc([cx - r * 0.85, cy - r * 0.1, cx + r * 0.45, cy + r * 0.9],
             90, 270, fill=RUST, width=w)
    draw.polygon([(cx - r * 0.85, cy + r * 0.4), (cx - r * 0.55, cy + r * 0.4),
                  (cx - r * 0.7, cy + r * 0.62)], fill=RUST)
    draw.line([cx - r * 0.85, cy + r * 0.85, cx + r * 0.85, cy + r * 0.85],
              fill=INK, width=w - 2 * SCALE)



def glyph_flame(draw, cx, cy, r):
    w = 6 * SCALE
    draw.polygon([(cx, cy - r * 0.95), (cx + r * 0.42, cy - r * 0.1),
                  (cx + r * 0.55, cy + r * 0.35), (cx + r * 0.3, cy + r * 0.85),
                  (cx - r * 0.3, cy + r * 0.85), (cx - r * 0.55, cy + r * 0.35),
                  (cx - r * 0.42, cy - r * 0.1)], fill=RUST)
    draw.polygon([(cx, cy - r * 0.45), (cx + r * 0.22, cy + r * 0.05),
                  (cx + r * 0.28, cy + r * 0.4), (cx, cy + r * 0.6),
                  (cx - r * 0.28, cy + r * 0.4), (cx - r * 0.22, cy + r * 0.05)],
                 fill=GOLD)
    draw.line([cx - r * 0.7, cy + r * 0.95, cx + r * 0.7, cy + r * 0.95],
              fill=INK, width=w - 2 * SCALE)


def glyph_atom(draw, cx, cy, r):
    w = 6 * SCALE
    import math
    for ang, col in ((0, INK), (60, TEAL), (120, PLUM)):
        th = math.radians(ang)
        pts = []
        for k in range(49):
            t = 2 * math.pi * k / 48
            x = r * 0.9 * math.cos(t)
            y = r * 0.36 * math.sin(t)
            pts.append((cx + x * math.cos(th) - y * math.sin(th),
                        cy + x * math.sin(th) + y * math.cos(th)))
        draw.line(pts, fill=col, width=w - 2 * SCALE, joint="curve")
    draw.ellipse([cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13],
                 fill=RUST)


def glyph_jet(draw, cx, cy, r):
    w = 6 * SCALE
    draw.polygon([(cx + r * 0.95, cy), (cx + r * 0.3, cy - r * 0.18),
                  (cx - r * 0.55, cy - r * 0.22), (cx - r * 0.9, cy - r * 0.42),
                  (cx - r * 0.72, cy), (cx - r * 0.9, cy + r * 0.42),
                  (cx - r * 0.55, cy + r * 0.22), (cx + r * 0.3, cy + r * 0.18)],
                 outline=INK, width=w)
    draw.polygon([(cx - r * 0.1, cy - r * 0.2), (cx + r * 0.15, cy - r * 0.75),
                  (cx + r * 0.3, cy - r * 0.2)], fill=RUST)
    draw.polygon([(cx - r * 0.1, cy + r * 0.2), (cx + r * 0.15, cy + r * 0.75),
                  (cx + r * 0.3, cy + r * 0.2)], fill=RUST)
    draw.line([cx - r * 0.9, cy, cx - r * 1.05, cy], fill=GOLD, width=w)
    burst(draw, cx - r * 0.15, cy - r * 0.85, r * 0.12, GOLD)


def glyph_magnifier(draw, cx, cy, r):
    w = 6 * SCALE
    draw.ellipse([cx - r * 0.62, cy - r * 0.85, cx + r * 0.42, cy + r * 0.19],
                 outline=INK, width=w)
    draw.ellipse([cx - r * 0.34, cy - r * 0.57, cx + r * 0.14, cy - r * 0.09],
                 outline=TEAL, width=w - 2 * SCALE)
    draw.line([cx + r * 0.3, cy + r * 0.07, cx + r * 0.85, cy + r * 0.62],
              fill=RUST, width=w)
    draw.line([cx + r * 0.72, cy + r * 0.5, cx + r * 0.95, cy + r * 0.73],
              fill=INK, width=w - SCALE)


def glyph_storm(draw, cx, cy, r):
    w = 6 * SCALE
    draw.ellipse([cx - r * 0.9, cy - r * 0.55, cx + r * 0.9, cy + r * 0.25],
                 outline=INK, width=w)
    draw.ellipse([cx - r * 0.5, cy - r * 0.95, cx + r * 0.45, cy - r * 0.15],
                 outline=INK, width=w)
    draw.line([cx - r * 0.75, cy + r * 0.25, cx + r * 0.75, cy + r * 0.25],
              fill=INK, width=w - SCALE)
    draw.polygon([(cx + r * 0.15, cy + r * 0.25), (cx - r * 0.25, cy + r * 0.65),
                  (cx + r * 0.05, cy + r * 0.65), (cx - r * 0.3, cy + r * 1.05),
                  (cx + r * 0.35, cy + r * 0.45), (cx + r * 0.05, cy + r * 0.45)],
                 fill=GOLD)


def glyph_megaphone(draw, cx, cy, r):
    w = 6 * SCALE
    draw.polygon([(cx - r * 0.75, cy - r * 0.35), (cx + r * 0.35, cy - r * 0.75),
                  (cx + r * 0.35, cy + r * 0.75), (cx - r * 0.75, cy + r * 0.35)],
                 outline=INK, width=w)
    draw.line([cx - r * 0.75, cy - r * 0.35, cx - r * 0.75, cy + r * 0.35],
              fill=RUST, width=w)
    draw.line([cx - r * 0.9, cy + r * 0.45, cx - r * 0.55, cy + r * 0.9],
              fill=INK, width=w - SCALE)
    draw.arc([cx + r * 0.45, cy - r * 0.5, cx + r * 0.95, cy + r * 0.5],
             270, 90, fill=TEAL, width=w - 2 * SCALE)
    draw.arc([cx + r * 0.6, cy - r * 0.25, cx + r * 0.8, cy + r * 0.25],
             270, 90, fill=TEAL, width=w - 2 * SCALE)


# ------------------------------------------------------------- stories
@dataclass
class Story:
    kicker: str
    accent: tuple
    headline: str
    standfirst: str
    glyph: object


LEAD = Story(
    "LEAD STORY · ELECTION",
    RUST,
    "New Zealand coalition loses its majority",
    ("Final results leave PM Luxon one seat short; the centre-right "
     "government now needs the centrist Opportunity Party to stay in power."),
    glyph_scales,
)

ROW_THREE = [
    Story("WEATHER · USA", SLATE,
          "Thanksgiving storm grounds 400 flights, cuts power to 724,000",
          "A powerful storm sweeps the US East on the holiday; more "
          "than 2,000 flights are delayed.",
          glyph_storm),
    Story("DISASTER · SPAIN", TEAL,
          "Diesel tanker sinks off Ibiza, one crew member dead",
          "The tanker, carrying up to 7,000 tonnes of diesel, capsizes; "
          "a slick spreads off the island.",
          glyph_boat),
    Story("GULF · KUWAIT", OCHRE,
          "Two Italians killed in drone strike in Kuwait",
          "The technicians were servicing air defences; Iran denies "
          "any role in the attack.",
          glyph_jet),
]

ROW_TWO = [
    Story("GULF · HORMUZ", RUST,
          "Iran reports blasts on three tankers in the Strait of Hormuz",
          "Explosions hit three ships in the world's busiest oil waterway "
          "as Gulf tensions climb.",
          glyph_flame),
    Story("USA · THANKSGIVING", PLUM,
          "Trump's Thanksgiving message lashes out at foes and migrants",
          "The president uses the holiday message to attack political "
          "rivals and the federal government.",
          glyph_megaphone),
]

TICKER = (
    "Zelensky warns of a new Russian mass strike in the coming days   \u00b7   "
    "Trump urges Putin to pull back military aggression   \u00b7   "
    "UK net migration falls to near a 30-year low   \u00b7   "
    "Argentina bans its central bank from printing money for the state   \u00b7   "
    "Delhi police free 164 foreigners in cyber-slavery bust   \u00b7   "
    "Bangkok oil depot blast injures seven, four critical   \u00b7   "
    "EU budget talks for 2028\u201334 end with no deal   \u00b7   "
    "All hostages freed after 16-hour supermarket siege in Colombia"
)


# ------------------------------------------------------------- cards
def card_height(draw, story, text_w, head_pt, body_pt, icon_r):
    head = face(SANS_BOLD, head_pt)
    body = face(SANS, body_pt)
    head_lines = fit_lines(draw, story.headline, head, text_w)
    body_lines = fit_lines(draw, story.standfirst, body, text_w)
    icon_space = max(icon_r * 2 + 20, 0)
    text_h = 56 + block_height(head, len(head_lines), 1.12) + 6 \
        + block_height(body, len(body_lines), 1.22) + 18
    return max(text_h, icon_space + 28)


def paint_card(draw, box, story, head_pt=26, body_pt=19, icon_r=52):
    x0, y0, x1, y1 = [v * SCALE for v in box]
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10 * SCALE,
                           fill=CARD, outline=INK, width=2 * SCALE)
    tag_chip(draw, x0 + 16 * SCALE, y0 + 14 * SCALE, story.kicker, story.accent)
    icon_cx = x1 - (icon_r + 20) * SCALE
    icon_cy = y0 + (y1 - y0) // 2 + 6 * SCALE
    story.glyph(draw, icon_cx, icon_cy, icon_r * SCALE)
    text_w = (x1 - x0) - 32 * SCALE - (icon_r * 2 + 30) * SCALE
    head = face(SANS_BOLD, head_pt)
    body = face(SANS, body_pt)
    top = y0 + 56 * SCALE
    top = paint_lines(draw, x0 + 16 * SCALE, top,
                      fit_lines(draw, story.headline, head, text_w),
                      head, INK, 1.12)
    paint_lines(draw, x0 + 16 * SCALE, top + 6 * SCALE,
                fit_lines(draw, story.standfirst, body, text_w),
                body, BODY_INK, 1.22)


def build():
    page = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(page)
    margin = 36
    y = 0

    # navy masthead band with the date in gold
    band_h = 116
    draw.rectangle([0, 0, CANVAS, band_h * SCALE], fill=NAVY)
    y = centred_line(draw, 14 * SCALE,
                     "T H E   W O R L D   I N   O N E   P I C T U R E",
                     face(SANS_BOLD, 19), (232, 228, 218))
    y = centred_line(draw, y + 2 * SCALE, "FRIDAY 27 NOVEMBER 2026",
                     face(SERIF_BOLD, 52), GOLD)
    draw.line([margin * SCALE, (band_h - 10) * SCALE,
               CANVAS - margin * SCALE, (band_h - 10) * SCALE],
              fill=GOLD, width=2 * SCALE)
    y = band_h + 8

    # lead story: glyph on the left, headline on the right
    lead_head = face(SANS_BOLD, 36)
    lead_body = face(SANS, 20)
    lead_text_w = (SIZE - 2 * margin - 260) * SCALE
    lead_head_lines = fit_lines(draw, LEAD.headline, lead_head, lead_text_w)
    lead_body_lines = fit_lines(draw, LEAD.standfirst, lead_body, lead_text_w)
    lead_h = 12 + 28 + 10 + block_height(lead_head, len(lead_head_lines), 1.1) \
        + 6 + block_height(lead_body, len(lead_body_lines), 1.22) + 12
    lx0, ly0, lx1, ly1 = margin, y, SIZE - margin, y + lead_h
    draw.rounded_rectangle([lx0 * SCALE, ly0 * SCALE, lx1 * SCALE, ly1 * SCALE],
                           radius=10 * SCALE, fill=CARD, outline=INK, width=3 * SCALE)
    tag_chip(draw, (lx0 + 216) * SCALE, ly0 * SCALE + 12 * SCALE,
             LEAD.kicker, LEAD.accent)
    LEAD.glyph(draw, (lx0 + 108) * SCALE,
                ly0 * SCALE + (lead_h // 2 + 10) * SCALE, 80 * SCALE)
    draw.line([(lx0 + 216) * SCALE, (ly0 + 12) * SCALE,
               (lx0 + 216) * SCALE, (ly1 - 12) * SCALE],
              fill=GOLD, width=2 * SCALE)
    top = ly0 * SCALE + 50 * SCALE
    top = paint_lines(draw, (lx0 + 232) * SCALE, top, lead_head_lines,
                      lead_head, INK, 1.1)
    paint_lines(draw, (lx0 + 232) * SCALE, top + 6 * SCALE, lead_body_lines,
                lead_body, BODY_INK, 1.22)
    y = ly1 + 5

    # three stories side by side
    gap = 10
    col_w = (SIZE - 2 * margin - 2 * gap) // 3
    inner_w = (col_w * SCALE - 32 * SCALE - (36 * 2 + 24) * SCALE)
    row_h = max(card_height(draw, s, inner_w, 20, 16, 36) for s in ROW_THREE)
    for i, story in enumerate(ROW_THREE):
        left = margin + i * (col_w + gap)
        paint_card(draw, [left, y, left + col_w, y + row_h], story,
                   head_pt=20, body_pt=16, icon_r=36)
    y += row_h + 5

    # two wider stories side by side
    col2_w = (SIZE - 2 * margin - gap) // 2
    inner2_w = (col2_w * SCALE - 32 * SCALE - (48 * 2 + 28) * SCALE)
    row2_h = max(card_height(draw, s, inner2_w, 24, 18, 48) for s in ROW_TWO)
    for i, story in enumerate(ROW_TWO):
        left = margin + i * (col2_w + gap)
        paint_card(draw, [left, y, left + col2_w, y + row2_h], story,
                   head_pt=24, body_pt=18, icon_r=48)
    y += row2_h + 5

    # navy ticker strip with the day's shorter items
    tick_font = face(SANS, 19)
    tick_lines = fit_lines(draw, TICKER, tick_font,
                           (SIZE - 2 * margin - 36) * SCALE)
    strip_h = 4 + 26 + 2 + block_height(tick_font, len(tick_lines), 1.25) + 4
    draw.rectangle([margin * SCALE, y * SCALE, (SIZE - margin) * SCALE,
                    (y + strip_h) * SCALE], fill=NAVY)
    draw.text(((margin + 16) * SCALE, (y + 9) * SCALE), "ALSO ON FRIDAY",
              font=face(SANS_BOLD, 19), fill=GOLD)
    paint_lines(draw, (margin + 16) * SCALE, (y + 38) * SCALE, tick_lines,
                tick_font, (242, 238, 226), 1.25)
    y += strip_h + 2

    centred_line(draw, y * SCALE,
                 "Drawn from Friday's reporting by Reuters, Al Jazeera, AP and "
                 "NDTV  \u00b7  27 November 2026",
                 face(SANS_ITALIC, 18), MUTED)
    print(f"layout ends at y={y + 26} of {SIZE}")

    page.resize((SIZE, SIZE), Image.LANCZOS).save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()

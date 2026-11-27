#!/usr/bin/env python3
"""Draw the 27 November 2026 broadsheet front page (1024x1024 PNG).

Paints at 2x (2048x2048) and downscales for crisp text. Pillow only,
no network, no downloaded images -- every glyph is drawn with shapes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersampling factor
W, H = 1024 * S, 1024 * S  # working canvas
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/liberation"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * S)

F_SERIF_BOLD = lambda s: font("LiberationSerif-Bold.ttf", s)
F_SANS_BOLD  = lambda s: font("LiberationSans-Bold.ttf", s)
F_SANS       = lambda s: font("LiberationSans-Regular.ttf", s)
F_SANS_ITAL  = lambda s: font("LiberationSans-Italic.ttf", s)

# Palette
NAVY   = (16, 34, 64)
NAVY2  = (24, 48, 88)
GOLD   = (212, 175, 55)
PAPER  = (247, 243, 232)
CARD   = (255, 255, 255)
INK    = (20, 20, 20)
GREY   = (90, 90, 90)
RULE   = (200, 192, 172)
RED    = (150, 30, 30)
BLUE   = (40, 90, 160)
TEAL   = (20, 120, 110)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

M = 40 * S          # page margin
CW = W - 2 * M      # content width

def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, lines, fnt, fill, spacing=None):
    """Draw lines; returns y just below the last line."""
    lh = fnt.size + (spacing if spacing is not None else int(6 * S))
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def card(x, y, w, h, outline=RULE):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10 * S,
                        fill=CARD, outline=outline, width=2 * S)

def kicker(x, y, label, color=RED):
    f = F_SANS_BOLD(15)
    d.text((x, y), label, font=f, fill=color)
    return y + f.size + 8 * S

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 96 * S], fill=NAVY)
d.rectangle([0, 96 * S, W, 100 * S], fill=GOLD)
title = "THE WORLD IN ONE PICTURE"
tf = F_SERIF_BOLD(40)
tw = d.textlength(title, font=tf)
d.text(((W - tw) / 2, 12 * S), title, font=tf, fill=(255, 255, 255))
date = "FRIDAY 27 NOVEMBER 2026"
df = F_SANS_BOLD(17)
dw = d.textlength(date, font=df)
d.text(((W - dw) / 2, 62 * S), date, font=df, fill=GOLD)

y = 116 * S

# ---------------------------------------------------------------- lead story
LEAD_H = 196 * S
card(M, y, CW, LEAD_H)
lx, ly = M + 22 * S, y + 16 * S
glyph_w = 250 * S
text_w = CW - 44 * S - glyph_w
ly = kicker(lx, ly, "LEAD STORY  ·  ELECTION")
hf = F_SERIF_BOLD(34)
head_lines = wrap("New Zealand coalition loses its majority", hf, text_w)
ly = text_block(lx, ly + 4 * S, head_lines, hf, INK, spacing=6 * S)
sf = F_SANS(19)
stand_lines = wrap(
    "Final results leave PM Luxon one seat short; the centre-right "
    "government now needs the centrist Opportunity Party to stay in power.",
    sf, text_w)
text_block(lx, ly + 8 * S, stand_lines, sf, GREY, spacing=5 * S)

# scales glyph (right side of lead card)
gx = M + CW - glyph_w + 20 * S
gy = y + 34 * S
gw, gh = 210 * S, 150 * S
cx = gx + gw // 2
d.line([cx, gy, cx, gy + gh - 30 * S], fill=NAVY, width=6 * S)          # post
d.line([gx + 10 * S, gy + 14 * S, gx + gw - 10 * S, gy + 14 * S],
       fill=NAVY, width=6 * S)                                          # beam
d.ellipse([cx - 8 * S, gy - 6 * S, cx + 8 * S, gy + 10 * S], fill=GOLD)  # finial
for side in (-1, 1):
    px = cx + side * (gw // 2 - 16 * S)
    d.line([px, gy + 14 * S, px, gy + 62 * S], fill=NAVY, width=4 * S)   # string
    d.polygon([(px - 42 * S, gy + 62 * S), (px + 42 * S, gy + 62 * S),
               (px, gy + 96 * S)], fill=GOLD, outline=NAVY)             # pan
d.line([gx + 10 * S, gy + gh - 12 * S, gx + gw - 10 * S, gy + gh - 12 * S],
       fill=NAVY, width=5 * S)                                          # base

y += LEAD_H + 18 * S

# ---------------------------------------------------------------- three cards
CARD3_W = (CW - 2 * 16 * S) // 3
CARD3_H = 248 * S

def storm_cloud(cx, cy, s):
    d.ellipse([cx - 70 * s, cy - 30 * s, cx + 10 * s, cy + 30 * s], fill=(90, 105, 130))
    d.ellipse([cx - 30 * s, cy - 45 * s, cx + 55 * s, cy + 25 * s], fill=(110, 125, 150))
    d.ellipse([cx + 5 * s, cy - 25 * s, cx + 75 * s, cy + 30 * s], fill=(90, 105, 130))
    d.polygon([(cx - 5 * s, cy + 20 * s), (cx + 15 * s, cy + 20 * s),
               (cx - 5 * s, cy + 55 * s), (cx + 20 * s, cy + 55 * s),
               (cx - 10 * s, cy + 95 * s), (cx - 15 * s, cy + 60 * s),
               (cx + 5 * s, cy + 60 * s)], fill=GOLD)

def boat(cx, cy, s):
    cx, cy = int(cx), int(cy)
    d.line([cx, int(cy - 70 * s), cx, int(cy + 10 * s)], fill=NAVY,
           width=int(5 * s))                                             # mast
    d.polygon([(int(cx + 6 * s), int(cy - 66 * s)), (int(cx + 6 * s), int(cy - 8 * s)),
               (int(cx + 62 * s), int(cy - 8 * s))], fill=(200, 60, 50))  # sail
    d.polygon([(int(cx - 78 * s), int(cy + 10 * s)), (int(cx + 78 * s), int(cy + 10 * s)),
               (int(cx + 58 * s), int(cy + 42 * s)), (int(cx - 58 * s), int(cy + 42 * s))],
              fill=NAVY)                                                 # hull
    for wx in (-60, -10, 40):
        d.arc([int(cx + wx * s), int(cy + 52 * s), int(cx + (wx + 34) * s),
               int(cy + 72 * s)], 0, 180, fill=BLUE, width=int(4 * s))    # waves

def jet(cx, cy, s):
    d.polygon([(cx - 80 * s, cy), (cx - 30 * s, cy - 18 * s),
               (cx + 55 * s, cy - 10 * s), (cx + 85 * s, cy),
               (cx + 55 * s, cy + 10 * s), (cx - 30 * s, cy + 18 * s)],
              fill=NAVY)                                                 # fuselage
    d.polygon([(cx - 10 * s, cy - 12 * s), (cx + 20 * s, cy - 52 * s),
               (cx + 32 * s, cy - 50 * s), (cx + 18 * s, cy - 8 * s)],
              fill=NAVY)                                                 # wing
    d.polygon([(cx - 55 * s, cy - 8 * s), (cx - 40 * s, cy - 38 * s),
               (cx - 28 * s, cy - 36 * s), (cx - 38 * s, cy - 4 * s)],
              fill=NAVY)                                                 # tail

stories3 = [
    ("WEATHER  ·  USA",
     "Thanksgiving storm grounds 400 flights, cuts power to 724,000",
     "A powerful storm sweeps the US East on the holiday; more than "
     "2,000 flights are delayed.",
     storm_cloud),
    ("DISASTER  ·  SPAIN",
     "Diesel tanker sinks off Ibiza, one crew member dead",
     "The tanker, carrying up to 7,000 tonnes of diesel, capsizes; "
     "a slick spreads off the island.",
     boat),
    ("GULF  ·  KUWAIT",
     "Two Italians killed in drone strike in Kuwait",
     "The technicians were servicing air defences; Iran denies any "
     "role in the attack.",
     jet),
]

for i, (kick, head, stand, glyph) in enumerate(stories3):
    x = M + i * (CARD3_W + 16 * S)
    card(x, y, CARD3_W, CARD3_H)
    tx, ty = x + 16 * S, y + 14 * S
    tw3 = CARD3_W - 32 * S
    ty = kicker(tx, ty, kick)
    hf3 = F_SERIF_BOLD(20)
    hl = wrap(head, hf3, tw3)
    ty = text_block(tx, ty + 2 * S, hl, hf3, INK, spacing=4 * S)
    sf3 = F_SANS(15)
    sl = wrap(stand, sf3, tw3)
    ty = text_block(tx, ty + 6 * S, sl, sf3, GREY, spacing=4 * S)
    # glyph centred in the remaining space
    gy3 = ty + 8 * S
    avail = y + CARD3_H - 12 * S - gy3
    if avail > 40 * S:
        glyph(x + CARD3_W // 2, gy3 + avail // 2 - 6 * S, S * 0.45)

y += CARD3_H + 18 * S

# ---------------------------------------------------------------- two wide cards
CARD2_W = (CW - 16 * S) // 2
CARD2_H = 190 * S

def flame(cx, cy, s):
    d.polygon([(cx, cy - 75 * s), (cx + 28 * s, cy - 25 * s),
               (cx + 52 * s, cy - 5 * s), (cx + 42 * s, cy + 30 * s),
               (cx + 15 * s, cy + 55 * s), (cx - 18 * s, cy + 55 * s),
               (cx - 42 * s, cy + 28 * s), (cx - 48 * s, cy - 8 * s),
               (cx - 22 * s, cy - 30 * s)],
              fill=(220, 90, 30))
    d.polygon([(cx, cy - 30 * s), (cx + 16 * s, cy),
               (cx + 10 * s, cy + 28 * s), (cx - 12 * s, cy + 28 * s),
               (cx - 16 * s, cy - 2 * s)], fill=GOLD)

def megaphone(cx, cy, s):
    d.polygon([(cx - 55 * s, cy - 18 * s), (cx + 25 * s, cy - 48 * s),
               (cx + 25 * s, cy + 48 * s), (cx - 55 * s, cy + 18 * s)],
              fill=RED)                                                  # cone
    d.rectangle([cx - 72 * s, cy - 16 * s, cx - 52 * s, cy + 16 * s],
                fill=NAVY)                                               # mouthpiece
    d.polygon([(cx - 30 * s, cy + 22 * s), (cx - 8 * s, cy + 22 * s),
               (cx - 14 * s, cy + 62 * s), (cx - 30 * s, cy + 62 * s)],
              fill=NAVY)                                                 # handle
    for r in (58, 74):
        d.arc([int(cx + 30 * s), int(cy - r * s), int(cx + 30 * s + 24 * s),
               int(cy + r * s)], -55, 55, fill=NAVY, width=int(5 * s))   # sound arcs

stories2 = [
    ("GULF  ·  HORMUZ",
     "Iran reports blasts on three tankers in the Strait of Hormuz",
     "Explosions hit three ships in the world's busiest oil waterway "
     "as Gulf tensions climb.",
     flame),
    ("USA  ·  THANKSGIVING",
     "Trump's Thanksgiving message lashes out at foes and migrants",
     "The president uses the holiday message to attack political "
     "rivals and the federal government.",
     megaphone),
]

for i, (kick, head, stand, glyph) in enumerate(stories2):
    x = M + i * (CARD2_W + 16 * S)
    card(x, y, CARD2_W, CARD2_H)
    tx, ty = x + 16 * S, y + 14 * S
    glyph_w2 = 150 * S
    tw2 = CARD2_W - 32 * S - glyph_w2
    ty = kicker(tx, ty, kick)
    hf2 = F_SERIF_BOLD(22)
    hl = wrap(head, hf2, tw2)
    ty = text_block(tx, ty + 2 * S, hl, hf2, INK, spacing=4 * S)
    sf2 = F_SANS(15)
    sl = wrap(stand, sf2, tw2)
    text_block(tx, ty + 6 * S, sl, sf2, GREY, spacing=4 * S)
    glyph(x + CARD2_W - glyph_w2 // 2 - 8 * S, y + CARD2_H // 2, S * 0.62)

y += CARD2_H + 18 * S

# ---------------------------------------------------------------- ticker
TICK_H = 132 * S
d.rectangle([M, y, M + CW, y + TICK_H], fill=NAVY)
d.rectangle([M, y, M + CW, y + TICK_H], outline=GOLD, width=2 * S)
tf2 = F_SANS_BOLD(16)
d.text((M + 16 * S, y + 12 * S), "ALSO ON FRIDAY", font=tf2, fill=GOLD)
items = [
    "Zelensky warns of a new Russian mass strike in the coming days",
    "Trump urges Putin to pull back military aggression",
    "UK net migration falls to near a 30-year low",
    "Argentina bans its central bank from printing money for the state",
    "Delhi police free 164 foreigners in cyber-slavery bust",
    "Bangkok oil depot blast injures seven, four critical",
    "EU budget talks for 2028–34 end with no deal",
    "All hostages freed after 16-hour supermarket siege in Colombia",
]
ticker_text = "  ·  ".join(items)
tf3 = F_SANS(16)
t_lines = wrap(ticker_text, tf3, CW - 32 * S)
ty = y + 38 * S
for ln in t_lines:
    d.text((M + 16 * S, ty), ln, font=tf3, fill=(255, 255, 255))
    ty += tf3.size + 5 * S

y += TICK_H + 14 * S

# ---------------------------------------------------------------- footer
ff = F_SANS_ITAL(14)
credit = ("Drawn from Friday's reporting by Reuters, Al Jazeera, AP "
          "and NDTV · 27 November 2026")
cw = d.textlength(credit, font=ff)
d.text(((W - cw) / 2, y), credit, font=ff, fill=GREY)

# ---------------------------------------------------------------- save
img = img.resize((1024, 1024), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")

#!/usr/bin/env python3
"""News Towers, round 3 REVISED - NI22 entry for @climaxku.

Rebuilt after the pixel-by-pixel dissection of the actual #1 entry
(BEDAH-TOP1, which overrides BEDAH-R3 where they conflict):

- NO certainty chips anywhere (#1 has zero). Card furniture is now a
  D1 slug bar on every card: full card width, region colour, white
  bold caps = PLACE/TOPIC + the card's biggest fact.
- Lead headlines back to ~18 px serif (Playfair 20, pitch 21);
  mini headlines ~13 px serif bold, two lines, no decks.
- Lead scenes ~110 px tall, one giant subject >=70% of scene height.
- 21 pictured cards: 3 leads + 18 deck-less minis (8 briefs were
  converted to minis), 16 briefs left, 37 stories total.
- Numbered circular badges on every scene; numbered map pins for
  ALL 37 stories, briefs included.
- Italic subdeck under the date masthead = the 3 lead headlines.
- Briefs in #1 format: region number badge + bold coloured region
  label + one line + (source). Pitch 13 px, font 11 px.
- Tally 16 px, labels INSIDE segments, widths proportional, sum 37.
- Scenes: flat vector, one gradient max, <=3 large elements; region
  colours are the mid-tone palette sampled from #1.
Stories only from POOL22-BARU v3. PIL only.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402  (bundled polygon data)

W = H = 1024
MX = 14
CW = W - 2 * MX
RED = (165, 40, 40)
INK = (30, 33, 40)
SOFT = (96, 96, 98)
PAPER = (247, 242, 232)
LINE = (198, 190, 170)
WHITE = (255, 255, 255)
BLACK = (26, 26, 26)

# Region colours: mid-tone palette sampled from the #1 entry, so all
# colours can coexist without neon noise (D12).
REGIONS = {
    "AMERICAS": (45, 88, 146),
    "EUROPE": (78, 128, 45),
    "MIDEAST": (181, 83, 39),
    "ASIA": (156, 46, 90),
    "OCEANIA": (54, 143, 145),
    "GLOBAL": (160, 130, 47),
}

FB = os.path.join(HERE, "fonts", "Archivo-Bold.ttf")
FM = os.path.join(HERE, "fonts", "Archivo-Medium.ttf")
FP = os.path.join(HERE, "fonts", "PlayfairDisplay-900.ttf")


def fB(s):
    return ImageFont.truetype(FB, s)


def fM(s):
    return ImageFont.truetype(FM, s)


def fP(s):
    return ImageFont.truetype(FP, s)


def wrap(d, text, font, maxw):
    out, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out


def put(d, xy, s, font, fill=INK, anchor=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def grad(d, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(1, h - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.line([x, y + i, x + w, y + i], fill=col)


def badge(d, cx, cy, dia, n, col):
    """Numbered circular badge, region colour, white number (D3)."""
    r = dia / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
              outline=WHITE, width=2)
    put(d, (cx, cy - dia * 0.28), str(n), fB(10 if dia >= 18 else 9),
        fill=WHITE, anchor="ma")


def slug_bar(d, x, y, w, h, col, text, fsize):
    """D1: full-width region-colour slug bar, white bold caps."""
    d.rectangle([x, y, x + w, y + h], fill=col)
    f = fB(fsize)
    while d.textlength(text, font=f) > w - 10 and fsize > 7:
        fsize -= 1
        f = fB(fsize)
    put(d, (x + 6, y + h // 2 - fsize * 0.36), text, f, fill=WHITE)


# ------------------------------------------------------------ lead scenes
# 110 px tall. One giant subject >=70% of scene height, one gradient,
# flat vector, <=3 large elements (D7 + D12). Defect fixes from the
# earlier r3 build are kept, rescaled: saturated Vegas dusk, filled
# Falcon frame, clean Anfield.

def lead_vegas(d, x, y, w, h):
    grad(d, x, y, w, h, (255, 128, 32), (196, 52, 84))
    rng = random.Random(7)
    base = y + h - 20
    towers = [(2, 78, 34), (40, 60, 26), (70, 84, 38), (196, 72, 32),
              (232, 88, 40), (276, 64, 30)]
    for tx, th, tw in towers:
        d.rectangle([x + tx, base - th, x + tx + tw, base],
                    fill=(38, 30, 52))
        for wy in range(base - th + 5, base - 4, 8):
            for wx in range(x + tx + 4, x + tx + tw - 4, 7):
                if rng.random() < 0.6:
                    d.rectangle([wx, wy, wx + 3, wy + 3],
                                fill=(255, 214, 92))
    nx = x + 148  # needle tower: ~92% of scene height
    d.polygon([(nx, base), (nx + 13, y + 10), (nx + 26, base)],
              fill=(30, 24, 46))
    d.ellipse([nx - 6, y + 2, nx + 32, y + 17], fill=(255, 190, 60))
    d.ellipse([nx + 4, y + 5, nx + 22, y + 13], fill=(255, 226, 130))
    d.rectangle([x, base, x + w, y + h], fill=(24, 22, 30))
    for i in range(0, w, 28):
        d.rectangle([x + i, y + h - 8, x + i + 14, y + h - 2],
                    fill=(235, 235, 228) if (i // 28) % 2 == 0 else RED)


def lead_falcon(d, x, y, w, h):
    grad(d, x, y, w, h, (28, 128, 235), (120, 196, 250))
    base = y + h - 12
    d.rectangle([x, base, x + w, y + h], fill=(52, 148, 62))
    cx = x + w // 2 - 14
    gx = cx + 40  # gantry
    d.rectangle([gx, y + 8, gx + 15, base], fill=(52, 58, 66))
    for yy in range(y + 13, base - 5, 11):
        d.line([gx, yy, gx + 15, yy + 8], fill=(52, 58, 66), width=3)
    d.rectangle([gx - 24, y + 28, gx, y + 33], fill=(52, 58, 66))
    # rocket body ~96 px of the 110 px scene (~87%)
    d.rectangle([cx - 22, y + 20, cx + 22, base], fill=(248, 248, 244),
                outline=(40, 44, 50), width=3)
    d.polygon([(cx - 22, y + 20), (cx, y + 2), (cx + 22, y + 20)],
              fill=(248, 248, 244), outline=(40, 44, 50))
    d.ellipse([cx - 5, y + 30, cx + 5, y + 40], fill=(40, 44, 50))
    d.rectangle([cx - 22, y + 52, cx + 22, y + 59], fill=(40, 44, 50))
    d.rectangle([cx - 22, base - 15, cx + 22, base - 6],
                fill=(40, 44, 50))
    d.polygon([(cx - 22, base), (cx - 38, base), (cx - 22, base - 17)],
              fill=(40, 44, 50))
    d.polygon([(cx + 22, base), (cx + 38, base), (cx + 22, base - 17)],
              fill=(40, 44, 50))
    for dx, r in [(-48, 12), (-24, 15), (26, 14), (50, 11)]:
        d.ellipse([cx + dx - r, base - 7, cx + dx + r, base + 3],
                  fill=(250, 250, 248))


def lead_anfield(d, x, y, w, h):
    grad(d, x, y, w, h, (24, 92, 168), (70, 140, 205))
    d.rectangle([x + 8, y + 12, x + w - 8, y + 44], fill=(168, 44, 34))
    d.polygon([(x, y + 13), (x + w, y + 13), (x + w - 14, y + 3),
               (x + 14, y + 3)], fill=(70, 44, 40))
    for r in range(3):
        d.line([x + 16, y + 20 + r * 8, x + w - 16, y + 20 + r * 8],
               fill=(226, 150, 130), width=3)
    for px in (x + 12, x + w - 30):
        d.line([px + 8, y + 44, px + 8, y + 6], fill=(26, 28, 34),
               width=4)
        d.rectangle([px, y + 1, px + 18, y + 10], fill=(255, 246, 190))
    py = y + 44  # pitch fills the lower 60%
    d.rectangle([x, py, x + w, y + h], fill=(24, 156, 52))
    for i in range(0, w, 54):
        d.rectangle([x + i, py, x + i + 27, y + h], fill=(34, 172, 62))
    d.line([x + w // 2, py, x + w // 2, y + h], fill=(245, 245, 238),
           width=3)
    d.ellipse([x + w // 2 - 15, y + h - 36, x + w // 2 + 15, y + h - 6],
              outline=(245, 245, 238), width=3)


# ------------------------------------------------------------ mini scenes
# 45 px tall, FULL-BLEED flat region-colour field edge to edge (D8),
# 1-3 large flat elements, no small device on a pale band (D12).
# In-scene data labels only when >=14 px.

def mini_scene(d, kind, x, y, w, h, col):
    d.rectangle([x, y, x + w, y + h], fill=col)
    cy = y + h // 2
    if kind == "radar":
        cx = x + w // 2
        for r in (13, 24, 35):
            d.arc([cx - r, cy - r, cx + r, cy + r], 180, 335,
                  fill=WHITE, width=3)
        d.line([cx, cy + 8, cx + 32, cy - 18], fill=(255, 220, 120),
               width=3)
        d.ellipse([cx + 14, y + 6, cx + 22, y + 14], fill=(255, 220, 120))
    elif kind == "burst":
        bx, by = x + w // 2, cy
        for a in range(0, 360, 30):
            r = 19 if a % 60 == 0 else 12
            d.line([bx, by, bx + r * math.cos(math.radians(a)),
                    by + r * math.sin(math.radians(a))],
                   fill=(255, 226, 110), width=4)
        d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=WHITE)
    elif kind == "gapbar":
        put(d, (x + 8, y + 3), "$120BN", fB(20), fill=WHITE)
        d.rectangle([x + 8, y + 30, x + w - 8, y + 39], fill=WHITE)
        d.rectangle([x + 8, y + 30, x + 8 + int((w - 16) * 0.38),
                     y + 39], fill=(255, 214, 80))
    elif kind == "seismo":  # clean redraw kept: one big trace, no overlap
        pts = []
        rng = random.Random(9)
        for i in range(52):
            amp = 2 if i < 18 or i > 36 else rng.randint(8, 17)
            pts.append((x + 6 + i * 2.9, cy + (amp if i % 2 else -amp)))
        d.line(pts, fill=WHITE, width=3)
    elif kind == "innings":
        put(d, (x + 8, y + 4), "720/9", fB(26), fill=WHITE)
        d.rectangle([x + 92, y + 12, x + w - 8, y + 22], fill=WHITE)
        d.rectangle([x + 92, y + 12, x + 92 + int((w - 100) * 0.8),
                     y + 22], fill=(255, 214, 80))
        put(d, (x + 92, y + 26), "DECLARED", fB(10), fill=WHITE)
    elif kind == "court":
        d.rectangle([x + 8, y + 5, x + w - 8, y + h - 5],
                    outline=WHITE, width=3)
        d.line([x + w // 2, y + 5, x + w // 2, y + h - 5], fill=WHITE,
               width=2)
        d.line([x + 8, cy, x + w - 8, cy], fill=WHITE, width=2)
        d.ellipse([x + w // 2 - 8, cy - 8, x + w // 2 + 8, cy + 8],
                  outline=WHITE, width=2)
    elif kind == "gauge":
        put(d, (x + 10, y + 8), "-18", fB(24), fill=WHITE)
        d.arc([x + w - 62, y + 2, x + w - 6, y + 58], 180, 360,
              fill=WHITE, width=5)
        d.line([x + w - 34, y + 30, x + w - 14, y + 10],
               fill=(255, 214, 80), width=4)
    elif kind == "dohyo":
        d.ellipse([x + w // 2 - 34, y + 2, x + w // 2 + 34, y + h - 2],
                  fill=(238, 214, 160), outline=WHITE, width=3)
        d.ellipse([x + w // 2 - 17, y + 12, x + w // 2 + 17, y + h - 12],
                  outline=(150, 110, 60), width=2)
    elif kind == "leaders":
        for i in range(3):
            bw = int((w - 20) * (0.95 - i * 0.18))
            d.rectangle([x + 10, y + 5 + i * 13, x + 10 + bw,
                         y + 14 + i * 13],
                        fill=WHITE if i == 0 else (205, 225, 240))
    elif kind == "yard":
        for i in range(7):
            d.line([x + 12 + i * 21, y + 3, x + 12 + i * 21, y + h - 3],
                   fill=WHITE, width=3)
        put(d, (x + 8, y + h - 15), "WK 12", fB(11),
            fill=(255, 226, 110))
    elif kind == "bignum":  # giant score number fills the field
        pass  # text drawn by caller via kind data below
    elif kind == "tanker":
        by = y + h - 10
        d.polygon([(x + 18, by - 14), (x + w - 26, by - 14),
                   (x + w - 12, by), (x + 30, by)], fill=(24, 26, 34))
        d.rectangle([x + 44, by - 24, x + 74, by - 14], fill=(24, 26, 34))
        d.rectangle([x + w - 62, by - 27, x + w - 48, by - 14],
                    fill=(24, 26, 34))
        d.line([x + 8, by + 4, x + w - 8, by + 4], fill=WHITE, width=2)
    elif kind == "drone":
        cx, cyy = x + w // 2, cy - 2
        d.rectangle([cx - 16, cyy - 6, cx + 16, cyy + 6],
                    fill=(24, 26, 34))
        for dx, dy in ((-30, -12), (30, -12), (-30, 10), (30, 10)):
            d.line([cx, cyy, cx + dx, cyy + dy], fill=(24, 26, 34),
                   width=3)
            d.ellipse([cx + dx - 8, cyy + dy - 3, cx + dx + 8,
                       cyy + dy + 3], outline=WHITE, width=2)
        d.line([cx, cyy + 6, cx, cyy + 14], fill=(255, 90, 60), width=3)
    elif kind == "ball":
        cx, cyy = x + w // 2, cy
        d.ellipse([cx - 15, cyy - 15, cx + 15, cyy + 15],
                  fill=(250, 250, 246), outline=(150, 40, 40), width=2)
        d.arc([cx - 11, cyy - 13, cx + 3, cyy + 13], 300, 60,
              fill=(190, 40, 40), width=2)
        d.arc([cx - 3, cyy - 13, cx + 11, cyy + 13], 120, 240,
              fill=(190, 40, 40), width=2)
        d.rectangle([x + 12, y + 8, x + 20, y + h - 8],
                    fill=(226, 196, 130))
        d.rectangle([x + w - 20, y + 8, x + w - 12, y + h - 8],
                    fill=(226, 196, 130))
    elif kind == "football":
        cx, cyy = x + w // 2, cy
        d.ellipse([cx - 34, cyy - 15, cx + 34, cyy + 15],
                  fill=(146, 84, 44))
        d.line([cx - 8, cyy, cx + 8, cyy], fill=WHITE, width=3)
        for i in range(-2, 3):
            d.line([cx + i * 4, cyy - 3, cx + i * 4, cyy + 3],
                   fill=WHITE, width=2)
    elif kind == "flag":
        d.rectangle([x + 14, y + 26, x + w - 14, y + h - 4],
                    fill=(240, 236, 220))
        d.line([x + w // 2, y + 4, x + w // 2, y + 34], fill=WHITE,
               width=3)
        d.polygon([(x + w // 2, y + 4), (x + w // 2 + 20, y + 9),
                   (x + w // 2, y + 15)], fill=(255, 90, 60))
        d.ellipse([x + w // 2 - 4, y + 32, x + w // 2 + 4, y + 40],
                  fill=(24, 26, 34))
    elif kind == "vs":
        put(d, (x + w // 2, y + 5), "VS", fB(28), fill=WHITE,
            anchor="ma")
        d.ellipse([x + 22, cy - 11, x + 44, cy + 11], fill=WHITE)
        d.ellipse([x + w - 44, cy - 11, x + w - 22, cy + 11],
                  fill=(24, 26, 34))


def big_num_scene(d, x, y, w, h, col, text):
    """Mini scene whose single element is a giant number (>=14 px)."""
    d.rectangle([x, y, x + w, y + h], fill=col)
    f = fB(30)
    while d.textlength(text, font=f) > w - 16:
        f = fB(f.size - 2)
    put(d, (x + w // 2, y + h // 2 - f.size * 0.36), text, f,
        fill=WHITE, anchor="ma")


# ------------------------------------------------------------------ data
LEADS = [
    dict(n=1, region="AMERICAS", place="LAS VEGAS, USA",
         slug="LAS VEGAS: 50 LAPS ON THE STRIP", scene=lead_vegas,
         tier="OFFICIAL", src="FORMULA1.COM",
         head="Vegas GP lights out on the Strip",
         deck="Round 22, 50 laps from 04:00 UTC - 20:00 Saturday "
              "night in Nevada, on the Strip Circuit."),
    dict(n=2, region="AMERICAS", place="VANDENBERG, USA",
         slug="VANDENBERG: FALCON 9 - B1097", scene=lead_falcon,
         tier="OFFICIAL", src="VSFB OFFICIAL",
         head="Falcon 9 set for NROL-136 launch",
         deck="Window 12:16-12:46 UTC from SLC-4E, Vandenberg; "
              "booster B1097 returns to Landing Zone 4."),
    dict(n=3, region="EUROPE", place="LIVERPOOL, ENGLAND",
         slug="ANFIELD: LIVERPOOL V MAN UTD", scene=lead_anfield,
         tier="OFFICIAL", src="PREMIERLEAGUE.COM",
         head="Liverpool host Man United at Anfield",
         deck="Matchweek 11, kick-off 16:30 UTC (23:30 WIB); Hull v "
              "Brighton opens Sunday at 14:00 UTC."),
]

# 18 minis (stories 4-21): slug -> scene -> 2-line headline with
# >=2 facts (no deck) -> region + source line. Stories 14-21 were
# briefs in the previous build, converted to pictured cards (D2).
MINIS = [
    dict(n=4, region="MIDEAST", slug="BAHRAIN: 2 RADARS CLAIMED",
         kind="radar", src="IRGC STATEMENT",
         head="IRGC claims two Patriot radars hit in Bahrain"),
    dict(n=5, region="MIDEAST", slug="MAKKAH: MISSILE DOWNED",
         kind="burst", src="ANADOLU",
         head="Missile downed near Makkah; sirens 23:43"),
    dict(n=6, region="GLOBAL", slug="ANTALYA: VOTE 06:00 GMT",
         kind="gapbar", src="REUTERS",
         head="COP31 final text tabled; vote set for 06:00 GMT"),
    dict(n=7, region="ASIA", slug="MYANMAR: M4.1 - 95 KM DEEP",
         kind="seismo", src="NCS VIA ANI",
         head="M4.1 quake hits Myanmar, 95 km deep"),
    dict(n=8, region="OCEANIA", slug="WELLINGTON: 720-9 DECLARED",
         kind="innings", src="IANS - AFP",
         head="India declare 720/9, a Wellington record total"),
    dict(n=9, region="EUROPE", slug="TURIN: ATP FINAL",
         kind="court", src="ATP",
         head="Alcaraz v Zverev: the ATP final in Turin"),
    dict(n=10, region="AMERICAS", slug="NAPLES: KIM LEADS AT -18",
         kind="gauge", src="LPGA.COM",
         head="Kim leads CME finale at -18; $4m to winner"),
    dict(n=11, region="ASIA", slug="FUKUOKA: TIED 12-2",
         kind="dohyo", src="JSA",
         head="Sumo leaders tied 12-2 before the final bouts"),
    dict(n=12, region="AMERICAS", slug="RSM: 3 SHARE -9",
         kind="leaders", src="REUTERS",
         head="Three share the RSM lead at -9 after rain"),
    dict(n=13, region="AMERICAS", slug="NFL: 11 GAMES SUNDAY",
         kind="yard", src="ESPN - NFL",
         head="NFL Week 12: 11 games across Sunday"),
    dict(n=14, region="OCEANIA", slug="WELLINGTON: NICHOLLS 175",
         kind="bignum", big="175", src="IANS - AFP",
         head="Nicholls 175 in NZ's 368, still 352 behind"),
    dict(n=15, region="OCEANIA", slug="WELLINGTON: BUMRAH 4-92",
         kind="ball", src="IANS - AFP",
         head="Bumrah 4-92, his best figures against NZ"),
    dict(n=16, region="MIDEAST", slug="HORMUZ: TANKER ATTACKED",
         kind="tanker", src="UKMTO",
         head="Tanker attacked near Hormuz (UKMTO)"),
    dict(n=17, region="MIDEAST", slug="KUWAIT: DRONE DOWNED",
         kind="drone", src="ANADOLU",
         head="Drone downed at Ali Al Salem base, Kuwait"),
    dict(n=18, region="AMERICAS", slug="NFL: VIKINGS AT 49ERS",
         kind="football", src="ESPN - NFL",
         head="Vikings at 49ers, 20:20 ET Sunday night game"),
    dict(n=19, region="OCEANIA", slug="WELLINGTON: RAHUL 136",
         kind="bignum", big="136", src="IANS - AFP",
         head="Rahul 136 anchors India's record innings"),
    dict(n=20, region="AMERICAS", slug="NAPLES: THITIKUL -17",
         kind="flag", src="LPGA.COM",
         head="Thitikul one back at -17 behind Kim"),
    dict(n=21, region="ASIA", slug="FUKUOKA: YUSHO DECIDER",
         kind="vs", src="JSA",
         head="Onosato v Hoshoryu decides the yusho"),
]

NUMBERS = [
    ("720/9", "INDIA DECLARE (8)"),
    ("50", "LAPS, VEGAS GP (1)"),
    ("12:16", "FALCON WINDOW (2)"),
    ("12-2", "SUMO LEADERS (11)"),
    ("-18", "KIM AT CME (10)"),
    ("11", "NFL GAMES (13)"),
]

TIMELINE = ("SUNDAY IN UTC - 02:40 IRGC GULF STATEMENT - 04:00 VEGAS "
            "GP LIGHTS OUT - 06:00 GMT COP31 ADOPTION - 09:00 SUMO "
            "FINAL BOUTS - 12:16 FALCON WINDOW - 16:30 ANFIELD KICK-OFF")

# 16 briefs (stories 22-37), #1 format (D5).
BRIEFS = [
    ("OCEANIA", "Pant 128 in the same record innings", "IANS"),
    ("OCEANIA", "Gill 98, Jaiswal 85 at Wellington", "IANS"),
    ("AMERICAS", "Yoshida shares second behind Kim", "LPGA"),
    ("ASIA", "Atamifuji 11-3, one off the lead", "JSA"),
    ("AMERICAS", "Thorbjornsen co-leads RSM at -9", "Reuters"),
    ("AMERICAS", "Penge shares the RSM lead at -9", "Reuters"),
    ("AMERICAS", "Neergaard-Petersen also -9 at RSM", "Reuters"),
    ("EUROPE", "Hull v Brighton, 14:00 UTC Sunday", "Premier League"),
    ("EUROPE", "Alcaraz fought back past Shelton", "ATP"),
    ("GLOBAL", "COP31 text recalls Dubai fossil deal", "Reuters"),
    ("GLOBAL", "COP31 objections closed 03:00 GMT", "Reuters"),
    ("MIDEAST", "Bahrain civil industry site burned", "Anadolu"),
    ("MIDEAST", "Makkah sirens at 23:43 Riyadh time", "Anadolu"),
    ("ASIA", "Myanmar quake depth logged 95 km", "NCS"),
    ("AMERICAS", "NROL-136 is NRO batch No. 15", "VSFB"),
    ("AMERICAS", "B1097 targets Landing Zone 4 return", "VSFB"),
]

# DATE CHECK: the three parts kept exactly as built in the earlier
# r3 (deeper than #1's - kept, not enlarged). The old chip-tier
# legend is gone because the chips are gone (D6).
LEFT_OUT = ("Lviv (20 Nov) - Peru M6.9 (20/21 Nov) - Berlin Coalition "
            "(19 Nov) - ICJ ruling (19 Nov) - FBI NCIC hack (19/20 Nov) "
            "- France march 82,500 (21 Nov) - CEPA signing (21 Nov) - "
            "Sparta II (21 Nov)")
NOT_YET = ("COP31 final adoption - session 06:00 GMT, no result yet - "
           "Liverpool v Man Utd - 16:30 UTC - ATP Turin final - Sun night")
UNCONF = ("IRGC claim: 2 Patriot radars destroyed - Tehran's claim, not "
          "independently confirmed - Houthi interception claim - "
          "attributed, contested")
DC_FOOT = ("Every story on this page happened, or was first reported, "
           "on Sunday 22 November 2026.")

# Numbered map pins for ALL 37 stories (D3): n -> (lon, lat, dx, dy).
PINS = {
    1: (-115.1, 36.1, 0, 0), 2: (-120.6, 34.7, -7, -4),
    3: (-2.96, 53.43, 0, 0), 4: (50.55, 26.23, 6, -5),
    5: (39.82, 21.42, 0, 0), 6: (30.71, 36.88, 0, 0),
    7: (94.62, 24.40, 0, 0), 8: (174.78, -41.29, -12, -6),
    9: (7.69, 45.07, 0, 0), 10: (-81.8, 26.15, -8, -6),
    11: (130.40, 33.59, -8, -6), 12: (-81.5, 31.2, 0, 0),
    13: (-98.0, 39.5, 0, 0), 14: (174.78, -41.29, 0, -8),
    15: (174.78, -41.29, 12, -6), 16: (56.5, 26.5, 4, 4),
    17: (47.8, 29.4, 0, 0), 18: (-121.97, 37.4, 6, 4),
    19: (174.78, -41.29, -12, 5), 20: (-81.8, 26.15, 8, 5),
    21: (130.40, 33.59, 8, 5), 22: (174.78, -41.29, 1, 6),
    23: (174.78, -41.29, 13, 5), 24: (-81.8, 26.15, -9, 6),
    25: (130.40, 33.59, -9, 6), 26: (-81.5, 31.2, -11, -5),
    27: (-81.5, 31.2, 11, -5), 28: (-81.5, 31.2, 0, 8),
    29: (-0.33, 53.74, 10, -4), 30: (7.69, 45.07, 11, 5),
    31: (30.71, 36.88, -11, 6), 32: (30.71, 36.88, 11, 6),
    33: (50.55, 26.23, -7, 6), 34: (39.82, 21.42, 10, 6),
    35: (94.62, 24.40, 11, 6), 36: (-120.6, 34.7, 8, 5),
    37: (-120.6, 34.7, -8, 6),
}
PIN_REGION = {}
for _c in LEADS + MINIS:
    PIN_REGION[_c["n"]] = _c["region"]
for _i, (_r, _t, _s) in enumerate(BRIEFS):
    PIN_REGION[22 + _i] = _r

TOTAL = len(LEADS) + len(MINIS) + len(BRIEFS)  # 37


def tally_counts():
    counts = {r: 0 for r in REGIONS}
    for c in LEADS + MINIS:
        counts[c["region"]] += 1
    for r, _t, _s in BRIEFS:
        counts[r] += 1
    return counts


def italic_line(text, font, fill, maxw):
    """Render one line of text sheared into italics (no italic font
    is bundled; Playfair is sheared -0.22 like a true italic slant)."""
    tmp = Image.new("RGBA", (2200, 80), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((30, 8), text, font=font, fill=fill)
    tmp = tmp.crop(tmp.getbbox())
    w0, h0 = tmp.size
    shear = 0.22
    tmp = tmp.transform((w0 + int(h0 * shear) + 4, h0),
                        Image.AFFINE, (1, shear, -shear * 8, 0, 1, 0),
                        resample=Image.BICUBIC)
    tmp = tmp.crop(tmp.getbbox())
    if tmp.size[0] > maxw:
        tmp = tmp.resize((maxw, int(tmp.size[1] * maxw / tmp.size[0])),
                         Image.LANCZOS)
    return tmp


def build():
    counts = tally_counts()
    assert sum(counts.values()) == TOTAL, (counts, TOTAL)
    assert len(PINS) == TOTAL and len(PIN_REGION) == TOTAL
    assert len(LEADS) + len(MINIS) == 21  # pictured cards (D2)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # claim bar (black) - paper name small; the DATE is the masthead
    d.rectangle([0, 0, W, 24], fill=BLACK)
    put(d, (MX, 5), "NEWS TOWERS", fB(13), fill=WHITE)
    put(d, (W - MX, 6), f"THE WORLD IN ONE DAY - {TOTAL} STORIES - "
        "6 REGIONS - EVERY ONE REPORTED ON SUNDAY 22 NOVEMBER 2026",
        fB(10), fill=(210, 210, 210), anchor="ra")

    # date masthead (R1, unchanged): caps ~88 px, 92.6% of width
    layer = Image.new("RGBA", (2300, 200), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10, 10), "SUNDAY 22 NOVEMBER 2026",
                               font=fP(150), fill=INK)
    layer = layer.crop(layer.getbbox())
    layer = layer.resize((948, 88), Image.LANCZOS)
    img.paste(layer, ((W - 948) // 2, 27), layer)
    d = ImageDraw.Draw(img, "RGBA")

    # D4 subdeck: one italic serif line = the 3 lead headlines
    sub = " - ".join(c["head"] for c in LEADS).replace(" - ", "  ·  ")
    sub_img = italic_line(sub, fP(20), INK, CW)
    img.paste(sub_img, ((W - sub_img.size[0]) // 2, 119), sub_img)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([MX, 146, W - MX, 146], fill=INK, width=2)

    # numbers strip (R2, as built): six story-bound numbers
    cellw = CW / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + cellw * i + cellw / 2
        put(d, (cx, 150), num, fB(36), fill=RED, anchor="ma")
        put(d, (cx, 191), lab, fB(9), fill=SOFT, anchor="ma")
    d.line([MX, 203, W - MX, 203], fill=LINE, width=1)

    # tally (D10): 16 px, labels INSIDE segments, widths proportional
    ty = 207
    x = float(MX)
    for r in ["MIDEAST", "EUROPE", "ASIA", "OCEANIA", "AMERICAS",
              "GLOBAL"]:
        segw = CW * counts[r] / TOTAL
        d.rectangle([x, ty, x + segw, ty + 16], fill=REGIONS[r])
        label = f"{r} {counts[r]}"
        if d.textlength(label, font=fB(10)) < segw - 6:
            put(d, (x + segw / 2, ty + 3), label, fB(10), fill=WHITE,
                anchor="ma")
        x += segw

    # one-line UTC timeline (kept from the earlier build, compressed)
    tf = fB(10)
    while d.textlength(TIMELINE, font=tf) > CW:
        tf = fB(tf.size - 1)
    put(d, (MX, 228), TIMELINE, tf, fill=SOFT)
    d.line([MX, 242, W - MX, 242], fill=LINE, width=1)

    # leads: slug 20 -> scene 110 -> caption -> headline ~18 -> deck
    ly, lw = 248, 324
    for i, c in enumerate(LEADS):
        x = MX + i * (lw + 12)
        col = REGIONS[c["region"]]
        slug_bar(d, x, ly, lw, 20, col, c["slug"], 12)
        c["scene"](d, x, ly + 20, lw, 110)
        badge(d, x + lw - 13, ly + 20 + 110 - 13, 20, c["n"], col)
        put(d, (x, ly + 136), f"{c['n']} - {c['place']} - {c['region']}",
            fB(10), fill=col)  # D11 numbered lead caption
        hy = ly + 152
        lines = wrap(d, c["head"], fP(20), lw)
        assert len(lines) <= 2, (c["n"], lines)
        for ln in lines:
            put(d, (x, hy), ln, fP(20), fill=INK)
            hy += 21
        dy = ly + 196
        for ln in wrap(d, c["deck"], fM(11), lw)[:2]:
            put(d, (x, dy), ln, fM(11), fill=(52, 54, 58))
            dy += 13
        put(d, (x, dy + 2), f"{c['tier']} - {c['src']}", fB(9),
            fill=SOFT)

    d.line([MX, 486, W - MX, 486], fill=INK, width=2)
    put(d, (MX, 492), "MORE FROM SUNDAY - STORIES 4-21", fB(12),
        fill=RED)

    # minis: 6 cols x 3 rows, pitch 95. slug 15 -> scene 45 ->
    # headline 2 lines (serif 14, pitch 13) -> region+source 8 px.
    mw = 159
    for idx, c in enumerate(MINIS):
        x = MX + (idx % 6) * (mw + 8)
        y = 508 + (idx // 6) * 96
        col = REGIONS[c["region"]]
        slug_bar(d, x, y, mw, 15, col, c["slug"], 9)
        if c["kind"] == "bignum":
            big_num_scene(d, x, y + 15, mw, 45, col, c["big"])
        else:
            mini_scene(d, c["kind"], x, y + 15, mw, 45, col)
        badge(d, x + mw - 10, y + 15 + 45 - 10, 17, c["n"], col)
        hy = y + 60
        lines = wrap(d, c["head"], fP(14), mw)
        assert len(lines) <= 2, (c["n"], lines)
        for ln in lines:
            put(d, (x, hy), ln, fP(14), fill=INK)
            hy += 12
        put(d, (x, y + 88), f"{c['region']} - {c['src']}", fB(8),
            fill=SOFT)

    d.line([MX, 798, W - MX, 798], fill=INK, width=2)
    put(d, (MX, 804), "WHERE IT HAPPENED - ALL 37 STORIES, PINNED BY "
        "NUMBER", fB(10), fill=RED)
    put(d, (524, 804), "ALSO ON SUNDAY - STORIES 22-37", fB(10),
        fill=RED)

    # map (left): light sea, tan land - the bright #1-style panel
    mapx, mapy, mapw, maph = MX, 816, 492, 92
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph],
                fill=(205, 225, 235))
    sx, sy = mapw / 360.0, maph / 133.0

    def proj(lon, lat):
        return (mapx + (lon + 180) * sx, mapy + (78 - lat) * sy)

    for polys in WORLD.values():
        for poly in polys.split("|"):
            pts = []
            for pair in poly.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) > 2:
                d.polygon(pts, fill=(222, 205, 180))
    for n in range(1, TOTAL + 1):
        lon, lat, dx, dy = PINS[n]
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        col = REGIONS[PIN_REGION[n]]
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col,
                  outline=WHITE, width=1)
        put(d, (px, py - 3), str(n), fB(7), fill=WHITE, anchor="ma")

    # DATE CHECK (left, under the map): three parts, as built before
    bx, by, bw = MX, 918, 492
    d.rectangle([bx, by, bx + bw, 1022], outline=RED, width=2)
    put(d, (bx + 8, by + 5), "DATE CHECK - WHAT THIS PAGE DID WITH "
        "22 NOV", fB(10), fill=RED)
    yy = by + 21
    for title, body in (("LEFT OUT - NOT 22 NOV: ", LEFT_OUT),
                        ("NOT YET - SAME DAY, UNFINISHED: ", NOT_YET),
                        ("UNCONFIRMED / CONTESTED: ", UNCONF)):
        for ln in wrap(d, title + body, fM(9), bw - 16):
            put(d, (bx + 8, yy), ln, fM(9), fill=INK)
            yy += 10
        yy += 2
    put(d, (bx + 8, yy), DC_FOOT, fB(8), fill=RED)

    # briefs (right): D5 format, pitch 13, font 11, one line each
    for i, (reg, txt, src) in enumerate(BRIEFS):
        n = 22 + i
        x, y = 524, 816 + i * 13
        col = REGIONS[reg]
        d.ellipse([x, y, x + 11, y + 11], fill=col)
        put(d, (x + 5.5, y + 2), str(n), fB(7), fill=WHITE, anchor="ma")
        lx = x + 15
        put(d, (lx, y), reg, fB(11), fill=col)
        tx = lx + d.textlength(reg, font=fB(11)) + 5
        line = txt + f" ({src})"
        f = fM(11)
        while d.textlength(line, font=f) > (W - MX) - tx and len(txt) > 8:
            txt = txt[:-1]
            line = txt.rstrip() + f" ({src})"
        put(d, (tx, y), line, f, fill=INK)

    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "entry-300.png"))
    img.quantize(colors=256, method=Image.MEDIANCUT).save(
        os.path.join(HERE, "entry.png"), optimize=True)
    print("stories:", TOTAL, "pictured:", len(LEADS) + len(MINIS),
          "briefs:", len(BRIEFS))
    print("tally:", counts, "sum:", sum(counts.values()))
    print("entry.png bytes:",
          os.path.getsize(os.path.join(HERE, "entry.png")))


if __name__ == "__main__":
    build()

#!/usr/bin/env python3
"""News Towers - NI22 challenger for @climaxku.

Builds entry.png (1024x1024) and entry-300.png locally with PIL only.
Hierarchy follows STUDY-first-glance R1-R8: the DATE is the masthead,
one red accent, three pictorial lead scenes, a data strip on every card,
a real-polygon world map in the bottom zone. Story pool: POOL22-BARU v3
(13 verified events of Sunday 22 November 2026 + named discards).
"""
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402  (polygon data asset)

W = H = 1024
MX = 14                      # side margin
CW = W - 2 * MX              # content width = 996
RED = (190, 30, 20)
INK = (32, 36, 43)
SOFT = (90, 92, 96)
CREAM = (246, 240, 223)
PAPER = (251, 247, 234)
LINE = (196, 188, 168)
NAVY = (38, 54, 74)

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
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK, anchor=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def chip(d, x, y, s, font, bg, fg=(255, 255, 255), pad=5):
    w = d.textlength(s, font=font) + 2 * pad
    d.rounded_rectangle([x, y, x + w, y + font.size + 5], 4, fill=bg)
    d.text((x + pad, y + 2), s, font=font, fill=fg)
    return w


# ---------------------------------------------------------------- scenes
def scene_vegas(d, x, y, w, h):
    """Lead 1: Las Vegas Strip Circuit skyline at night."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 52))
    rng = random.Random(11)
    for _ in range(46):
        sx, sy = x + rng.randint(3, w - 3), y + rng.randint(2, 34)
        d.point((sx, sy), fill=(210, 214, 200))
    d.ellipse([x + w - 52, y + 6, x + w - 30, y + 28], fill=(226, 222, 196))
    # tower silhouettes (muted slate / sand)
    towers = [(6, 34, 26), (34, 22, 18), (56, 40, 30), (92, 26, 20),
              (150, 30, 24), (182, 18, 16), (238, 36, 28), (272, 24, 18)]
    base = y + h - 15
    for tx, th, tw in towers:
        d.rectangle([x + tx, base - th, x + tx + tw, base], fill=(74, 84, 104))
        for wy in range(base - th + 5, base - 4, 7):
            for wx in range(x + tx + 3, x + tx + tw - 3, 6):
                if rng.random() < 0.55:
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(232, 205, 130))
    # needle tower (Stratosphere-like)
    nx = x + 118
    d.polygon([(nx, base), (nx + 7, y + 10), (nx + 14, base)], fill=(96, 106, 128))
    d.ellipse([nx - 3, y + 4, nx + 17, y + 14], fill=(150, 160, 180))
    # track foreground with kerb
    d.rectangle([x, base, x + w, y + h], fill=(16, 20, 30))
    d.line([x, base + 4, x + w, base + 1], fill=(210, 210, 200), width=2)
    for i in range(0, w, 26):
        d.rectangle([x + i, y + h - 5, x + i + 12, y + h - 2],
                    fill=(200, 200, 192) if (i // 26) % 2 == 0 else (120, 60, 55))


def scene_falcon(d, x, y, w, h):
    """Lead 2: Falcon 9 on the pad at Vandenberg SLC-4E."""
    for i in range(h):
        t = i / h
        col = (int(168 - 60 * t), int(188 - 52 * t), int(214 - 40 * t))
        d.line([x, y + i, x + w, y + i], fill=col)
    base = y + h - 15
    d.rectangle([x, base, x + w, y + h], fill=(104, 110, 96))  # pad apron
    # distant coastal hills (low, so the rocket stays the subject)
    d.polygon([(x, base), (x + 70, base - 7), (x + 140, base),
               (x + 210, base - 6), (x + w, base)], fill=(122, 134, 118))
    cx = x + w // 2
    # launch tower gantry
    gx = cx + 30
    d.rectangle([gx, y + 8, gx + 11, base], fill=(70, 76, 84))
    for yy in range(y + 12, base - 4, 10):
        d.line([gx, yy, gx + 11, yy + 8], fill=(70, 76, 84), width=2)
    d.rectangle([gx - 19, y + 26, gx, y + 30], fill=(70, 76, 84))
    # rocket body (wide, outlined so it reads at thumbnail size)
    d.rectangle([cx - 11, y + 18, cx + 11, base], fill=(240, 240, 236),
                outline=(52, 56, 62), width=2)
    d.polygon([(cx - 11, y + 18), (cx, y + 2), (cx + 11, y + 18)],
              fill=(240, 240, 236), outline=(52, 56, 62))
    d.rectangle([cx - 11, base - 15, cx + 11, base - 9], fill=(52, 56, 62))
    d.rectangle([cx - 11, y + 44, cx + 11, y + 50], fill=(52, 56, 62))
    d.polygon([(cx - 11, base), (cx - 19, base), (cx - 11, base - 13)], fill=(52, 56, 62))
    d.polygon([(cx + 11, base), (cx + 19, base), (cx + 11, base - 13)], fill=(52, 56, 62))
    # vapour clouds at the base
    for dx, r in [(-28, 8), (-13, 10), (14, 9), (28, 7)]:
        d.ellipse([cx + dx - r, base - 5, cx + dx + r, base + 3], fill=(240, 240, 238))


def scene_anfield(d, x, y, w, h):
    """Lead 3: Anfield stadium towers and floodlights, evening."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 66, 84))
    base = y + h - 15
    # stand block with roof
    d.rectangle([x + 18, y + 26, x + w - 18, base - 12], fill=(96, 88, 84))
    d.polygon([(x + 10, y + 28), (x + w - 10, y + 28), (x + w - 24, y + 16),
               (x + 24, y + 16)], fill=(64, 60, 58))
    for r in range(3):
        d.line([x + 24, y + 36 + r * 7, x + w - 24, y + 36 + r * 7],
               fill=(150, 140, 128), width=2)
    # floodlight pylons
    for px in (x + 14, x + w - 20):
        d.line([px + 3, base - 10, px + 3, y + 6], fill=(30, 34, 40), width=3)
        for lx in range(3):
            for ly in range(2):
                d.rectangle([px + lx * 5, y + 2 + ly * 5, px + lx * 5 + 4,
                             y + 5 + ly * 5], fill=(250, 244, 200))
        d.polygon([(px - 4, y + 14), (px + 16, y + 14), (px + 30, base - 12),
                   (px - 18, base - 12)], fill=(255, 250, 210))
    # pitch foreground
    d.rectangle([x, base - 12, x + w, y + h], fill=(62, 110, 62))
    for i in range(0, w, 44):
        d.rectangle([x + i, base - 12, x + i + 22, y + h], fill=(70, 120, 70))
    d.line([x + w // 2, base - 12, x + w // 2, y + h], fill=(235, 235, 225), width=2)


# ------------------------------------------------------- mini strip art
def strip_device(d, kind, x, y, w, h, label):
    """One data device per mini card, drawn inside its 30px strip."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 231, 210))
    if kind == "radar":  # concentric arcs + blips
        cx, cy = x + 26, y + h - 2
        for r in (8, 16, 24):
            d.arc([cx - r, cy - r, cx + r, cy + r], 180, 330, fill=(110, 120, 110), width=2)
        d.ellipse([x + 40, y + 7, x + 45, y + 12], fill=(120, 90, 60))
        d.ellipse([x + 58, y + 15, x + 63, y + 20], fill=(120, 90, 60))
    elif kind == "arc":  # missile arc + intercept burst
        d.arc([x + 6, y + 4, x + 96, y + 44], 180, 300, fill=(110, 110, 120), width=2)
        bx, by = x + 82, y + 8
        for a in range(0, 360, 45):
            import math
            d.line([bx, by, bx + 8 * math.cos(math.radians(a)),
                    by + 8 * math.sin(math.radians(a))], fill=(150, 120, 60), width=2)
        d.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(90, 90, 100))
    elif kind == "doc":  # final-text document lines + seal
        d.rectangle([x + 8, y + 4, x + 30, y + h - 4], fill=(250, 250, 246),
                    outline=(120, 120, 110))
        for i in range(3):
            d.line([x + 12, y + 9 + i * 6, x + 26, y + 9 + i * 6], fill=(130, 130, 125), width=2)
        d.ellipse([x + 20, y + h - 11, x + 27, y + h - 4], outline=(150, 120, 60), width=2)
    elif kind == "wave":  # seismograph trace
        pts, rng = [], random.Random(4)
        for i in range(60):
            amp = 3 if i < 22 or i > 40 else rng.randint(6, 12)
            pts.append((x + 6 + i * 1.6, y + h / 2 + (amp if i % 2 else -amp)))
        d.line(pts, fill=(90, 100, 90), width=2)
    elif kind == "score":  # innings bar with wicket ticks
        d.rectangle([x + 6, y + 11, x + 96, y + 19], fill=(110, 128, 96))
        for i in range(9):
            d.line([x + 14 + i * 9, y + 8, x + 14 + i * 9, y + 22], fill=(70, 84, 60), width=2)
    elif kind == "court":  # tennis court top view
        d.rectangle([x + 8, y + 4, x + 92, y + h - 4], fill=(96, 118, 140),
                    outline=(240, 240, 235))
        d.line([x + 50, y + 4, x + 50, y + h - 4], fill=(240, 240, 235), width=2)
        d.line([x + 8, y + h / 2, x + 92, y + h / 2], fill=(240, 240, 235), width=1)
    elif kind == "gauge":  # golf gauge to -18
        d.rectangle([x + 6, y + 12, x + 96, y + 19], fill=(205, 198, 175))
        d.rectangle([x + 6, y + 12, x + 84, y + 19], fill=(96, 122, 84))
        for i in range(6):
            d.line([x + 12 + i * 16, y + 9, x + 12 + i * 16, y + 12], fill=(90, 90, 85), width=1)
    elif kind == "dohyo":  # sumo ring top view
        d.ellipse([x + 10, y + 2, x + 38, y + h - 2], fill=(206, 188, 150),
                  outline=(120, 100, 70), width=2)
        d.ellipse([x + 19, y + 9, x + 29, y + 19], outline=(120, 100, 70), width=1)
    elif kind == "board":  # three co-leader bars at -9
        for i, wd in enumerate((66, 66, 66)):
            d.rectangle([x + 6, y + 4 + i * 9, x + 6 + wd, y + 9 + i * 9],
                        fill=(104, 116, 96) if i == 0 else (140, 148, 132))
    elif kind == "yard":  # american football yard lines
        d.rectangle([x + 4, y + 3, x + 100, y + h - 3], fill=(96, 124, 88))
        for i in range(6):
            d.line([x + 12 + i * 16, y + 3, x + 12 + i * 16, y + h - 3],
                   fill=(240, 240, 232), width=2)
    text(d, (x + 106, y + h / 2), label, fB(10), fill=INK, anchor="lm")


# ------------------------------------------------------------------ data
# Cards 1-3 are the leads (pool events 6, 7, 8). Cards 4-13 are the other
# ten pool events in pool order. All facts come from POOL22-BARU v3 only.
LEADS = [
    dict(n=1, region="AMERICAS · FORMULA 1", rc=(122, 92, 46),
         src="FORMULA1.COM", scene=scene_vegas,
         chip="04:00 UTC · 50 LAPS", band="LAS VEGAS · STRIP CIRCUIT · ROUND 22",
         head="Las Vegas GP: lights out on the Strip Circuit",
         deck="Round 22 under lights: 50 laps from 04:00 UTC, 20:00 Saturday "
              "local time in Nevada."),
    dict(n=2, region="AMERICAS · SPACEFLIGHT", rc=(70, 97, 126),
         src="VSFB OFFICIAL", scene=scene_falcon,
         chip="12:16-12:46 UTC · B1097 TO LZ4", band="VANDENBERG · SLC-4E · NROL-136",
         head="Falcon 9 NROL-136 set for Vandenberg launch",
         deck="Window 12:16-12:46 UTC from SLC-4E; booster B1097 returns "
              "to Landing Zone 4."),
    dict(n=3, region="EUROPE · FOOTBALL", rc=(62, 107, 94),
         src="PREMIERLEAGUE.COM", scene=scene_anfield,
         chip="16:30 UTC · MATCHWEEK 11", band="ANFIELD · LIVERPOOL · SUNDAY",
         head="Liverpool host Man United at Anfield",
         deck="Matchweek 11, kick-off 16:30 UTC; Hull v Brighton opens "
              "Sunday at 14:00 UTC."),
]

MINIS = [
    dict(n=4, region="MIDEAST · CONFLICT", rc=(122, 92, 46), src="CLAIM · IRGC",
         kind="radar", lab="2 RADARS",
         head="IRGC claims strike on two Bahrain Patriot radars",
         deck="Al-Riffa and Awali radars targeted, says Tehran; a civil "
              "site burned, Res 2817 invoked."),
    dict(n=5, region="MIDEAST · AIR DEFENCE", rc=(122, 92, 46),
         src="ANADOLU", kind="arc", lab="01:42 CONFIRMED",
         head="Houthi missile intercepted bound for Makkah",
         deck="Sirens at 23:43 Riyadh time; coalition confirmed the "
              "interception near 01:42 local."),
    dict(n=6, region="GLOBAL · CLIMATE", rc=(95, 115, 80), src="REUTERS",
         kind="doc", lab="$120BN GAP",
         head="COP31 final text tabled, vote set 06:00 GMT",
         deck="Kurum tabled the package; objections closed 03:00 GMT, "
              "$120bn adaptation goal fell Thu."),
    dict(n=7, region="ASIA · EARTHQUAKE", rc=(94, 103, 124), src="NCS VIA ANI",
         kind="wave", lab="M4.1 · 95 KM",
         head="M4.1 quake strikes Myanmar, 95 km deep",
         deck="Depth 95 km; epicentre 24.404N, 94.616E, logged by "
              "India's NCS on 22 November."),
    dict(n=8, region="OCEANIA · CRICKET", rc=(62, 107, 94), src="IANS · AFP",
         kind="score", lab="720/9 DECLARED",
         head="India declare 720/9 - a Wellington record",
         deck="Rahul 136, Pant 128; highest Test total ever in NZ, "
              "352 ahead of NZ's 368."),
    dict(n=9, region="EUROPE · TENNIS", rc=(110, 85, 112), src="ATP · REUTERS",
         kind="court", lab="FINAL · TURIN",
         head="Alcaraz v Zverev for the Turin title",
         deck="Sunday final near 16:00 UTC; Alcaraz fought back past "
              "Shelton to reach it."),
    dict(n=10, region="AMERICAS · GOLF", rc=(95, 115, 80), src="LPGA.COM",
         kind="gauge", lab="-18 LEADS",
         head="Kim leads CME finale at -18 in Naples",
         deck="One clear of Thitikul and Yoshida at Tiburon; winner "
              "takes $4m, a women's record."),
    dict(n=11, region="ASIA · SUMO", rc=(94, 103, 124),
         src="JAPAN SUMO ASSOC.", kind="dohyo", lab="12-2 x2",
         head="Sumo finale: two leaders tied at 12-2",
         deck="Bouts near 09:00 UTC in Fukuoka: Onosato v Hoshoryu, "
              "Wakamotoharu v Atamifuji."),
    dict(n=12, region="AMERICAS · GOLF", rc=(95, 115, 80),
         src="REUTERS", kind="board", lab="3 AT -9",
         head="RSM round 3 moved to Sunday by rain",
         deck="Thorbjornsen, Penge, Neergaard-Petersen share -9; "
              "Sunday tees 14:10-16:00 UTC."),
    dict(n=13, region="AMERICAS · NFL", rc=(70, 97, 126), src="ESPN · NFL",
         kind="yard", lab="11 GAMES",
         head="NFL Week 12: 11 games on Sunday",
         deck="Early window 18:00 UTC; late games 16:05 ET; Vikings "
              "at 49ers at 20:20 ET."),
]

NUMBERS = [  # (digit, label, card it binds to)
    ("720/9", "INDIA DECLARE, WELLINGTON (8)", 8),
    ("50", "LAPS, LAS VEGAS GP (1)", 1),
    ("12:16", "UTC FALCON WINDOW OPENS (2)", 2),
    ("12-2", "SUMO CO-LEADERS (11)", 11),
    ("-18", "KIM LEADS CME FINALE (10)", 10),
    ("11", "NFL SUNDAY GAMES (13)", 13),
]

TIMELINE = [
    ("02:40 UTC", "IRGC statement on Gulf claim (4)"),
    ("04:00 UTC", "Las Vegas GP lights out (1)"),
    ("06:00 GMT", "COP31 approval session (6)"),
    ("09:00 UTC", "Sumo final bouts, Fukuoka (11)"),
    ("12:16 UTC", "Falcon 9 window opens (2)"),
    ("16:30 UTC", "Liverpool v Man Utd (3)"),
]

BRIEFS = [  # stories 14-40, each with a name or number, pool facts only
    "14 Rahul 136 in India's record 720/9 (IANS)",
    "15 Pant 128 in the same Wellington innings (IANS)",
    "16 Gill 98, Jaiswal 85 in the 720/9 (AFP)",
    "17 Nicholls 175 in New Zealand's 368 (IANS)",
    "18 Bumrah 4-92, best figures vs NZ (AFP)",
    "19 Thitikul one back at -17, Naples (LPGA)",
    "20 Yoshida shares 2nd, one behind Kim (ESPN/AP)",
    "21 Onosato v Hoshoryu: a yusho decider (JSA)",
    "22 Atamifuji 11-3, one win off the lead (JSA)",
    "23 Thorbjornsen co-leads RSM at -9 (Reuters)",
    "24 Penge shares the RSM lead at -9 (PGA Tour)",
    "25 Neergaard-Petersen also -9 (Reuters)",
    "26 RSM final round pushed to Monday (PGA Tour)",
    "27 Vikings at 49ers, night game 20:20 ET (ESPN)",
    "28 NFL late window from 16:05 ET Sunday (NFL)",
    "29 Hull v Brighton opens Sunday, 14:00 UTC (PL)",
    "30 Alcaraz fought back past Shelton (ATP)",
    "31 COP31 text recalls Dubai deal (Reuters)",
    "32 COP31 objections closed 03:00 GMT (Reuters)",
    "33 Drone downed at Ali Al Salem, Kuwait (BDF)",
    "34 Tanker attacked near Hormuz (UKMTO)",
    "35 Bahrain civil industry site burned (MoI)",
    "36 Makkah sirens at 23:43 Riyadh time (Anadolu)",
    "37 Myanmar quake depth logged at 95 km (NCS)",
    "38 NROL-136: NRO batch No. 15 (VSFB)",
    "39 Northrop Grumman built payload (SpaceX)",
    "40 B1097 targets Landing Zone 4 return (VSFB)",
]

DATECHECK = ("Left out as not 22 Nov news: Lviv strikes (20 Nov) · Peru M6.9 "
             "quake (20/21 Nov) · Berlin Coalition of the Willing (19 Nov) · "
             "ICJ ruling (19 Nov) · FBI NCIC hack reports (19/20 Nov) · "
             "France march of 82,500 (21 Nov) · CEPA signing (21 Nov) · "
             "Sparta II incident (21 Nov). Not yet: Davis Cup final (29 Nov).")

PINS = {  # card number -> (lon, lat)
    1: (-115.1, 36.1), 2: (-120.6, 34.7), 3: (-2.96, 53.43),
    4: (50.55, 26.23), 5: (39.82, 21.42), 6: (30.71, 36.88),
    7: (94.62, 24.40), 8: (174.78, -41.29), 9: (7.69, 45.07),
    10: (-81.8, 26.15), 11: (130.40, 33.59), 12: (-81.5, 31.2),
    13: (-122.4, 37.8),
}
BRIEF_DOTS = [(174.8, -41.3), (-81.8, 26.2), (130.4, 33.6), (-81.5, 31.2),
              (-122.4, 37.8), (-0.33, 53.74), (7.7, 45.1), (30.7, 36.9),
              (47.97, 29.38), (56.5, 26.5), (50.5, 26.2), (39.8, 21.4),
              (94.6, 24.4), (-120.6, 34.7)]


# ------------------------------------------------------------------ build
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")

    # R1: paper name as a thin bar (13px), date is the masthead.
    text(d, (MX, 5), "NEWS TOWERS", fB(13), fill=INK)
    text(d, (W - MX, 7), "THE WORLD IN ONE PICTURE · 40 STORIES · 6 REGIONS",
         fB(10), fill=SOFT, anchor="ra")
    d.line([MX, 24, W - MX, 24], fill=INK, width=2)

    # Date layer: rendered large, cropped to ink, scaled to 948x88.
    layer = Image.new("RGBA", (2300, 200), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((10, 10), "SUNDAY 22 NOVEMBER 2026", font=fP(150), fill=INK)
    layer = layer.crop(layer.getbbox())
    layer = layer.resize((948, 88), Image.LANCZOS)
    img.paste(layer, ((W - 948) // 2, 28), layer)
    d = ImageDraw.Draw(img, "RGBA")
    text(d, (W // 2, 121), "ONE PAGE · EVERY STORY DATED SUNDAY 22 NOVEMBER 2026 · "
         "CONTESTED CLAIMS ARE ATTRIBUTED", fB(11), fill=SOFT, anchor="ma")

    # R2: numbers strip, single red accent, digits 32px, top 22%.
    d.line([MX, 140, W - MX, 140], fill=LINE, width=1)
    text(d, (MX, 144), "THE DAY IN NUMBERS", fB(10), fill=RED)
    cellw = CW / 6
    for i, (num, lab, _c) in enumerate(NUMBERS):
        cx = MX + cellw * i + cellw / 2
        text(d, (cx, 146), num, fB(42), fill=RED, anchor="ma")
        text(d, (cx, 192), lab, fB(9), fill=SOFT, anchor="ma")
    d.line([MX, 208, W - MX, 208], fill=LINE, width=1)

    # UTC timeline, 6 slots, sharing the strip zone.
    tw = CW / 6
    for i, (tm, ev) in enumerate(TIMELINE):
        x = MX + tw * i
        text(d, (x + 2, 211), tm, fB(11), fill=INK)
        for j, ln in enumerate(wrap(d, ev, fM(9), tw - 8)[:2]):
            text(d, (x + 2, 226 + j * 11), ln, fM(9), fill=SOFT)
        if i:
            d.line([x, 212, x, 244], fill=LINE, width=1)

    # Leads: 3 pictorial scenes, 88px tall, data chip + caption band inside.
    ly, lw = 250, 324
    for i, c in enumerate(LEADS):
        x = MX + i * (lw + 12)
        c["scene"](d, x, ly, lw, 88)
        chip(d, x + 8, ly + 8, c["chip"], fB(10), NAVY)
        tw2 = d.textlength(c["src"], font=fB(9)) + 10
        d.rounded_rectangle([x + lw - tw2 - 6, ly + 8, x + lw - 6, ly + 23], 3,
                            fill=(250, 248, 240))
        text(d, (x + lw - 11, ly + 11), c["src"], fB(9), fill=INK, anchor="ra")
        d.rectangle([x, ly + 73, x + lw, ly + 88], fill=NAVY)
        text(d, (x + lw / 2, ly + 76), c["band"], fB(10),
             fill=(245, 242, 232), anchor="ma")
        text(d, (x, ly + 92), f"{c['n']}  {c['region']}", fB(10), fill=c["rc"])
        yy = ly + 106
        for ln in wrap(d, c["head"], fB(20), lw)[:2]:
            text(d, (x, yy), ln, fB(20), fill=INK)
            yy += 21
        yy += 2
        for ln in wrap(d, c["deck"], fM(12), lw)[:2]:
            text(d, (x, yy), ln, fM(12), fill=(52, 54, 58))
            yy += 15

    # Mini cards: 10 cards, 5 x 2, each with a 30px data strip + source tag.
    my, mw, mh = 436, 192, 116
    for idx, c in enumerate(MINIS):
        x = MX + (idx % 5) * (mw + 9)
        y = my + (idx // 5) * (mh + 10)
        strip_device(d, c["kind"], x, y, mw, 30, c["lab"])
        text(d, (x, y + 34), f"{c['n']}  {c['region']}", fB(9), fill=c["rc"])
        text(d, (x + mw, y + 34), c["src"], fB(9), fill=SOFT, anchor="ra")
        yy = y + 46
        for ln in wrap(d, c["head"], fB(14), mw)[:2]:
            text(d, (x, yy), ln, fB(14), fill=INK)
            yy += 17
        for ln in wrap(d, c["deck"], fM(12), mw)[:3]:
            text(d, (x, yy + 1), ln, fM(12), fill=(52, 54, 58))
            yy += 14

    # Bottom zone: map (left) + DATE CHECK / giant stats (right).
    by = 686
    text(d, (MX, by), "WHERE IT HAPPENED", fB(12), fill=INK)
    mapx, mapy, mapw, maph = MX, by + 18, 486, 160
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(30, 46, 40))
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
                d.polygon(pts, fill=(104, 138, 104))
    for lon, lat in BRIEF_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(210, 205, 180))
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        if n == 1:
            px += 5
        if n == 2:
            px -= 5
        if n == 4:
            px += 4
        if n == 5:
            px -= 4
        if n == 10:
            py += 7
        if n == 12:
            py -= 7
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=NAVY,
                  outline=(245, 242, 232), width=2)
        text(d, (px, py - 6), str(n), fB(10), fill=(255, 255, 255), anchor="ma")
    text(d, (MX, mapy + maph + 5),
         "Numbered pins = the 13 pictured cards · small dots = the briefs",
         fB(10), fill=SOFT)
    text(d, (MX, mapy + maph + 19),
         "Map drawn from real country polygons; pins sit on each story's place.",
         fM(10), fill=SOFT)

    rx, rw = 514, W - MX - 514
    d.rectangle([rx, by, rx + rw, by + 82], outline=RED, width=2)
    text(d, (rx + 8, by + 6), "DATE CHECK", fB(12), fill=RED)
    yy = by + 24
    for ln in wrap(d, DATECHECK, fM(10), rw - 16):
        text(d, (rx + 8, yy), ln, fM(10), fill=INK)
        yy += 13
    gy = by + 96
    text(d, (rx, gy), "BOUND TO THIS PAGE", fB(11), fill=INK)
    stats = [("720/9", "India's total (8)"),
             ("$4M", "CME prize (10)"),
             ("95 KM", "Quake depth (7)"),
             ("06:00", "GMT COP31 vote (6)")]
    for i, (num, lab) in enumerate(stats):
        x = rx + i * (rw / 4)
        y = gy + 16
        d.line([x, y, x + rw / 4 - 10, y], fill=NAVY, width=3)
        text(d, (x, y + 4), num, fP(20), fill=INK)
        text(d, (x, y + 27), lab, fM(9), fill=SOFT)

    # ALSO ON: 27 briefs in 4 columns x 7 lines.
    ay = 902
    d.line([MX, ay - 6, W - MX, ay - 6], fill=INK, width=2)
    text(d, (MX, ay), "ALSO ON SUNDAY 22 NOVEMBER - 27 MORE STORIES",
         fB(11), fill=INK)
    colw = CW / 4
    for i, b in enumerate(BRIEFS):
        x = MX + (i // 7) * colw
        y = ay + 20 + (i % 7) * 12
        text(d, (x, y), b, fM(10), fill=(52, 54, 58))
    text(d, (MX, 1008), "Every story happened, or was first reported, on Sunday "
         "22 November 2026. Sources named beside each story · Original drawings.",
         fM(9), fill=SOFT)

    img300 = img.resize((300, 300), Image.LANCZOS)
    img300.save(os.path.join(HERE, "entry-300.png"))
    out = img.quantize(colors=224, method=Image.MEDIANCUT)
    out.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("entry.png bytes:", os.path.getsize(os.path.join(HERE, "entry.png")))


if __name__ == "__main__":
    build()

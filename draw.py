#!/usr/bin/env python3
"""News Towers - NI22 round 4 hybrid for @climaxku.

Round-4 idea: keep the round-2 page (13 pictured cards + briefs,
R1-R8 hierarchy, deep DATE CHECK) and bolt on only the cheap wins:
a proportional region tally bar, fact-bearing slug bars on every
pictured card, an italic subdeck under the date, numbered badges on
every scene and numbered map pins for every story. The round-3
tile-wall conversion is deliberately NOT repeated, and the round-2
defects (dark lead band, colliding seismograph label, empty COP31
strip, duplicated stats row) are designed out here.

Run: python3 draw.py   (writes entry.png + entry-300.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PH = 1024, 1024
EDGE = 24
RED = (178, 34, 30)
INK = (26, 24, 20)
GREY = (96, 90, 80)
PAPER = (246, 240, 223)
WHITE = (255, 255, 255)

# region -> (label, colour)
REGIONS = {
    "AMERICAS": (70, 110, 160),
    "MIDEAST": (190, 110, 40),
    "EUROPE": (70, 130, 80),
    "ASIA": (150, 60, 110),
    "OCEANIA": (40, 140, 140),
    "GLOBAL": (120, 105, 40),
}

def F(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

def ab(s): return F("Archivo-Bold.ttf", s)
def am(s): return F("Archivo-Medium.ttf", s)
def pf(s): return F("PlayfairDisplay-900.ttf", s)

def put(dr, xy, s, font, fill=INK, anchor=None):
    dr.text(xy, s, font=font, fill=fill, anchor=anchor)

def fit(dr, s, font, maxw):
    """Shrink a copy of the string (ellipsis) until it fits maxw."""
    if dr.textlength(s, font=font) <= maxw:
        return s
    while s and dr.textlength(s + "...", font=font) > maxw:
        s = s[:-1]
    return s.rstrip() + "..."

def wrap(dr, s, font, maxw, limit=9):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if dr.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
            if len(lines) == limit:
                return lines
    if cur:
        lines.append(cur)
    return lines[:limit]

# ---------------------------------------------------------------- stories
# (num, region, source, slug, headline, deck, pin lon/lat)
LEADS = [
    (1, "AMERICAS", "FORMULA1.COM", "LAS VEGAS: 50 LAPS FROM 04:00 UTC",
     "Las Vegas GP: lights out on the Strip Circuit",
     "Round 22 under lights: 50 laps from 04:00 UTC, 20:00 Saturday local in Nevada.",
     (-115.1, 36.1)),
    (2, "AMERICAS", "VSFB OFFICIAL", "VANDENBERG: B1097 RETURNS TO LZ4",
     "Falcon 9 NROL-136 set for Vandenberg launch",
     "Window 12:16-12:46 UTC from SLC-4E; booster B1097 returns to Landing Zone 4.",
     (-120.6, 34.7)),
    (3, "EUROPE", "PREMIERLEAGUE.COM", "ANFIELD: MATCHWEEK 11, 16:30 UTC",
     "Liverpool host Man United at Anfield",
     "Matchweek 11, kick-off 16:30 UTC; Hull v Brighton opens Sunday at 14:00 UTC.",
     (-2.96, 53.43)),
]
MINIS = [
    (4, "MIDEAST", "CLAIM - IRGC", "BAHRAIN: 2 PATRIOT RADARS CLAIMED", "radar",
     "IRGC claims strike on two Bahrain Patriot radars",
     "Al-Riffa and Awali radars targeted, says Tehran; a civil site burned, Res 2817 invoked.",
     (50.55, 26.23)),
    (5, "MIDEAST", "ANADOLU", "MAKKAH: MISSILE DOWNED 01:42", "arc",
     "Houthi missile intercepted bound for Makkah",
     "Sirens at 23:43 Riyadh time; coalition confirmed the interception near 01:42 local.",
     (39.82, 21.42)),
    (6, "GLOBAL", "REUTERS", "ANTALYA: $120BN GAP IN TEXT", "gapbar",
     "COP31 final text tabled, vote set 06:00 GMT",
     "Kurum tabled the package; objections closed 03:00 GMT, $120bn adaptation goal fell Thu.",
     (30.71, 36.88)),
    (7, "ASIA", "NCS VIA ANI", "MYANMAR: M4.1 AT 95 KM DEEP", "wave",
     "M4.1 quake strikes Myanmar, 95 km deep",
     "Depth 95 km; epicentre 24.404N, 94.616E, logged by India's NCS on 22 November.",
     (94.62, 24.40)),
    (8, "OCEANIA", "IANS - AFP", "WELLINGTON: 720/9 DECLARED", "score",
     "India declare 720/9 - a Wellington record",
     "Rahul 136, Pant 128; highest Test total ever in NZ, 352 ahead of NZ's 368.",
     (174.78, -41.29)),
    (9, "EUROPE", "ATP - REUTERS", "TURIN: ALCARAZ V ZVEREV FINAL", "court",
     "Alcaraz v Zverev for the Turin title",
     "Sunday final near 16:00 UTC; Alcaraz fought back past Shelton to reach it.",
     (7.69, 45.07)),
    (10, "AMERICAS", "LPGA.COM", "NAPLES: KIM LEADS AT -18", "gauge",
     "Kim leads CME finale at -18 in Naples",
     "One clear of Thitikul and Yoshida at Tiburon; winner takes $4m, a women's record.",
     (-81.8, 26.15)),
    (11, "ASIA", "JAPAN SUMO ASSOC.", "FUKUOKA: TWO LEADERS AT 12-2", "dohyo",
     "Sumo finale: two leaders tied at 12-2",
     "Bouts near 09:00 UTC in Fukuoka: Onosato v Hoshoryu, Wakamotoharu v Atamifuji.",
     (130.40, 33.59)),
    (12, "AMERICAS", "REUTERS", "RSM: THREE SHARE LEAD AT -9", "board",
     "RSM round 3 moved to Sunday by rain",
     "Thorbjornsen, Penge, Neergaard-Petersen share -9; Sunday tees 14:10-16:00 UTC.",
     (-81.5, 31.2)),
    (13, "AMERICAS", "ESPN - NFL", "NFL: 11 GAMES ON SUNDAY", "yard",
     "NFL Week 12: 11 games on Sunday",
     "Early window 18:00 UTC; late games 16:05 ET; Vikings at 49ers at 20:20 ET.",
     (-122.4, 37.8)),
]
# briefs: (num, region, text, pin lon/lat)
BRIEFS = [
    (14, "OCEANIA", "Rahul 136 in India's record 720/9 (IANS)", (174.9, -41.0)),
    (15, "OCEANIA", "Pant 128 in the same Wellington innings (IANS)", (174.6, -41.6)),
    (16, "OCEANIA", "Gill 98, Jaiswal 85 in the 720/9 (AFP)", (175.1, -40.8)),
    (17, "OCEANIA", "Nicholls 175 in New Zealand's 368 (IANS)", (174.4, -41.9)),
    (18, "OCEANIA", "Bumrah 4-92, best figures vs NZ (AFP)", (175.3, -41.3)),
    (19, "AMERICAS", "Thitikul one back at -17, Naples (LPGA)", (-81.6, 26.4)),
    (20, "AMERICAS", "Yoshida shares 2nd, one behind Kim (ESPN/AP)", (-82.0, 25.9)),
    (21, "ASIA", "Onosato v Hoshoryu: a yusho decider (JSA)", (130.6, 33.8)),
    (22, "ASIA", "Atamifuji 11-3, one win off the lead (JSA)", (130.2, 33.4)),
    (23, "AMERICAS", "Thorbjornsen co-leads RSM at -9 (Reuters)", (-81.3, 31.5)),
    (24, "AMERICAS", "Penge shares the RSM lead at -9 (PGA Tour)", (-81.7, 30.9)),
    (25, "AMERICAS", "Neergaard-Petersen also -9 (Reuters)", (-81.1, 31.8)),
    (26, "AMERICAS", "RSM final round pushed to Monday (PGA Tour)", (-81.9, 31.3)),
    (27, "AMERICAS", "Vikings at 49ers, night game 20:20 ET (ESPN)", (-122.2, 38.0)),
    (28, "AMERICAS", "NFL late window from 16:05 ET Sunday (NFL)", (-100.0, 39.0)),
    (29, "EUROPE", "Hull v Brighton opens Sunday, 14:00 UTC (PL)", (-0.33, 53.74)),
    (30, "EUROPE", "Alcaraz fought back past Shelton (ATP)", (7.9, 45.3)),
    (31, "GLOBAL", "COP31 text recalls Dubai deal (Reuters)", (30.9, 37.1)),
    (32, "GLOBAL", "COP31 objections closed 03:00 GMT (Reuters)", (30.5, 36.6)),
    (33, "MIDEAST", "Drone downed at Ali Al Salem, Kuwait (BDF)", (47.97, 29.38)),
    (34, "MIDEAST", "Tanker attacked near Hormuz (UKMTO)", (56.5, 26.5)),
    (35, "MIDEAST", "Bahrain civil industry site burned (MoI)", (50.4, 26.0)),
    (36, "MIDEAST", "Makkah sirens at 23:43 Riyadh time (Anadolu)", (39.6, 21.2)),
    (37, "ASIA", "Myanmar quake depth logged at 95 km (NCS)", (94.4, 24.7)),
    (38, "AMERICAS", "NROL-136: NRO batch No. 15 (VSFB)", (-120.4, 34.9)),
    (39, "AMERICAS", "Northrop Grumman built payload (SpaceX)", (-120.8, 34.5)),
    (40, "AMERICAS", "B1097 targets Landing Zone 4 return (VSFB)", (-120.2, 35.1)),
]
NUMBERS = [("720/9", "INDIA DECLARE (8)"), ("50", "VEGAS LAPS (1)"),
           ("12:16", "FALCON WINDOW (2)"), ("12-2", "SUMO LEADERS (11)"),
           ("-18", "KIM, CME (10)"), ("11", "NFL GAMES (13)")]
TIMELINE = "02:40 IRGC statement (4)  ·  04:00 Vegas lights out (1)  ·  " \
           "06:00 GMT COP31 vote (6)  ·  09:00 Sumo finals (11)  ·  " \
           "12:16 Falcon window (2)  ·  16:30 Liverpool v Man Utd (3)"

TOTAL = len(LEADS) + len(MINIS) + len(BRIEFS)
TALLY = {}
for _, reg, *_ in LEADS + MINIS:
    TALLY[reg] = TALLY.get(reg, 0) + 1
for _, reg, _, _ in BRIEFS:
    TALLY[reg] = TALLY.get(reg, 0) + 1
assert sum(TALLY.values()) == TOTAL == 40, (TALLY, TOTAL)
TALLY_ORDER = ["AMERICAS", "MIDEAST", "OCEANIA", "ASIA", "EUROPE", "GLOBAL"]

# ---------------------------------------------------------------- scenes
def badge(dr, x, y, num, colour, dia=18):
    dr.ellipse([x, y, x + dia, y + dia], fill=colour, outline=WHITE, width=2)
    put(dr, (x + dia / 2, y + dia / 2 - 1), str(num), ab(10 if dia < 20 else 11),
        fill=WHITE, anchor="mm")

def scene_vegas(dr, box):
    x0, y0, x1, y1 = box; h = y1 - y0
    for i in range(h):  # dusk gradient: one bright orange field
        t = i / h
        dr.line([(x0, y0 + i), (x1, y0 + i)],
                fill=(int(240 - 90 * t), int(140 - 60 * t), int(50 + 20 * t)))
    import random; rng = random.Random(7)
    bx = x0 + 8
    while bx < x1 - 90:  # skyline blocks
        bw = rng.randint(16, 30); bh = rng.randint(22, 48)
        dr.rectangle([bx, y1 - bh, bx + bw, y1], fill=(52, 44, 60))
        for wy in range(y1 - bh + 5, y1 - 5, 8):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rng.random() < .6:
                    dr.point((wx, wy), fill=(255, 220, 120))
        bx += bw + 5
    nx = x1 - 62  # needle tower, dominant subject
    dr.polygon([(nx, y1), (nx + 10, y0 + 8), (nx + 20, y1)], fill=(40, 36, 52))
    dr.ellipse([nx + 2, y0 + 4, nx + 18, y0 + 20], fill=(255, 90, 70))
    dr.rectangle([x0, y1 - 7, x1, y1], fill=(30, 30, 34))
    dr.line([(x0, y1 - 7), (x1, y1 - 7)], fill=WHITE, width=2)

def scene_falcon(dr, box):
    x0, y0, x1, y1 = box
    dr.rectangle(box, fill=(86, 150, 205))  # bright sky field
    dr.rectangle([x0, y1 - 16, x1, y1], fill=(96, 130, 70))
    cx = (x0 + x1) // 2 - 40  # rocket body, ~85% of scene height
    dr.rectangle([cx, y0 + 16, cx + 26, y1 - 14], fill=WHITE, outline=INK)
    dr.polygon([(cx, y0 + 16), (cx + 13, y0 + 3), (cx + 26, y0 + 16)], fill=(210, 60, 50))
    dr.rectangle([cx + 34, y0 + 10, cx + 40, y1 - 14], fill=(70, 70, 78))  # gantry
    for gy in range(y0 + 18, y1 - 16, 12):
        dr.line([(cx + 26, gy), (cx + 40, gy)], fill=(70, 70, 78), width=2)
    dr.ellipse([cx - 16, y1 - 20, cx + 44, y1 - 6], fill=(235, 235, 235))

def scene_anfield(dr, box):
    x0, y0, x1, y1 = box
    dr.rectangle([x0, y0, x1, y0 + 46], fill=(168, 44, 40))  # red stand
    for r in range(5):
        dr.line([(x0, y0 + 8 + r * 8), (x1, y0 + 8 + r * 8)], fill=(230, 190, 170), width=2)
    dr.rectangle([x0, y0 + 46, x1, y1], fill=(52, 150, 66))  # bright pitch
    for i in range(6):
        if i % 2 == 0:
            dr.rectangle([x0 + i * (x1 - x0) // 6, y0 + 46,
                          x0 + (i + 1) * (x1 - x0) // 6, y1], fill=(62, 165, 74))
    dr.line([(x0, y1 - 4), (x1, y1 - 4)], fill=WHITE, width=2)
    for fx in (x0 + 18, x1 - 24):  # floodlight pylons
        dr.line([(fx, y0 + 30), (fx, y0 + 2)], fill=INK, width=3)
        dr.rectangle([fx - 7, y0, fx + 7, y0 + 7], fill=(255, 240, 160), outline=INK)

def mini_scene(dr, box, kind):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; cy = (y0 + y1) // 2
    if kind == "radar":
        dr.rectangle(box, fill=(58, 84, 120))
        for r in (8, 16, 25):
            dr.arc([x0 + 14 - r, cy - r, x0 + 14 + r, cy + r], -60, 60, fill=(140, 220, 255), width=3)
        dr.rectangle([x0 + 10, cy - 3, x0 + 18, cy + 3], fill=WHITE)
        put(dr, (x1 - 30, cy), "2 RADARS", ab(13), fill=WHITE, anchor="rm")
    elif kind == "arc":
        dr.rectangle(box, fill=(44, 62, 104))
        dr.arc([x0 + 20, y0 + 6, x1 - 70, y1 + 26], 180, 300, fill=(255, 170, 60), width=4)
        dr.polygon([(x1 - 62, y0 + 12), (x1 - 50, y0 + 22), (x1 - 66, y0 + 24)], fill=(255, 220, 120))
        put(dr, (x1 - 30, cy), "01:42", ab(14), fill=WHITE, anchor="rm")
    elif kind == "gapbar":  # filled bar, never an empty strip
        dr.rectangle(box, fill=(240, 236, 220))
        dr.rectangle([x0 + 8, cy - 10, x0 + 8 + int((w - 110) * .78), cy + 10], fill=(70, 130, 80))
        dr.rectangle([x0 + 8 + int((w - 110) * .78), cy - 10, x1 - 102, cy + 10],
                     outline=RED, width=2)
        put(dr, (x1 - 30, cy), "$120BN", ab(14), fill=RED, anchor="rm")
    elif kind == "wave":  # waveform confined to left 55%; label zone kept clear
        dr.rectangle(box, fill=(238, 240, 244))
        pts = []
        for i in range(46):
            xx = x0 + 8 + i * (w * .42) / 46
            amp = 3 if i < 16 else (13 if i < 26 else 5)
            pts.append((xx, cy + (amp if i % 2 else -amp)))
        dr.line(pts, fill=(40, 60, 120), width=2)
        put(dr, (x1 - 30, cy), "M4.1 - 95 KM", ab(11), fill=(40, 60, 120), anchor="rm")
    elif kind == "score":
        dr.rectangle(box, fill=(52, 130, 74))
        put(dr, ((x0 + x1) / 2, cy), "720/9", pf(24), fill=WHITE, anchor="mm")
    elif kind == "court":
        dr.rectangle(box, fill=(70, 110, 170))
        dr.rectangle([x0 + 14, y0 + 5, x1 - 14, y1 - 5], outline=WHITE, width=2)
        dr.line([(x0 + 14, cy), (x1 - 14, cy)], fill=WHITE, width=2)
        dr.line([((x0 + x1) / 2, y0 + 5), ((x0 + x1) / 2, y1 - 5)], fill=WHITE, width=1)
    elif kind == "gauge":
        dr.rectangle(box, fill=(250, 244, 224))
        dr.arc([x0 + 12, y0 + 4, x0 + 62, y0 + 54], 180, 360, fill=(70, 130, 80), width=5)
        dr.line([(x0 + 37, cy + 8), (x0 + 54, cy - 6)], fill=RED, width=3)
        put(dr, (x1 - 30, cy), "-18", pf(22), fill=INK, anchor="rm")
    elif kind == "dohyo":
        dr.rectangle(box, fill=(214, 188, 148))
        dr.ellipse([x0 + 16, y0 + 3, x0 + 66, y1 - 3], outline=(120, 84, 40), width=4)
        put(dr, (x1 - 30, cy), "12-2 x2", ab(13), fill=(90, 60, 24), anchor="rm")
    elif kind == "board":
        dr.rectangle(box, fill=(238, 246, 238))
        for i, nm in enumerate(("THORBJORNSEN", "PENGE", "NEERGAARD-P.")):
            yy = y0 + 4 + i * 11
            dr.rectangle([x0 + 8, yy, x0 + 96, yy + 9], fill=(70, 130, 80))
            put(dr, (x0 + 11, yy + 4), nm, ab(8), fill=WHITE, anchor="lm")
        put(dr, (x1 - 30, cy), "3 AT -9", ab(12), fill=(40, 90, 50), anchor="rm")
    elif kind == "yard":
        dr.rectangle(box, fill=(52, 120, 66))
        for i in range(1, 6):
            xx = x0 + i * w // 6
            dr.line([(xx, y0), (xx, y1)], fill=WHITE, width=2)
        put(dr, ((x0 + x1) / 2, cy), "11", pf(22), fill=WHITE, anchor="mm")

# ---------------------------------------------------------------- layout
def slug_bar(dr, x, y, w, colour, text, size=10):
    dr.rectangle([x, y, x + w, y + 16], fill=colour)
    put(dr, (x + 7, y + 8), fit(dr, text, ab(size), w - 14), ab(size), fill=WHITE, anchor="lm")
    return y + 16

def italic_line(img, y, s):
    """Render one serif line sheared into italics, centred."""
    layer = Image.new("RGBA", (PW, 30), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    f = pf(19)
    ld.text((PW / 2, 15), s, font=f, fill=INK + (255,), anchor="mm")
    sheared = layer.transform(layer.size, Image.AFFINE, (1, 0.22, -0.22 * 15, 0, 1, 0))
    img.paste(sheared, (0, y), sheared)

def build():
    img = Image.new("RGB", (PW, PH), PAPER)
    dr = ImageDraw.Draw(img)

    put(dr, (EDGE, 5), "NEWS TOWERS", ab(13), fill=INK)
    put(dr, (PW - EDGE, 6), "THE WORLD IN ONE PICTURE - 40 STORIES - 6 REGIONS",
        ab(10), fill=GREY, anchor="ra")

    # R1 date masthead: own layer, scaled to 948x88 ink box
    layer = Image.new("L", (2600, 220), 0)
    ImageDraw.Draw(layer).text((0, 0), "SUNDAY 22 NOVEMBER 2026", font=pf(150), fill=255)
    layer = layer.crop(layer.getbbox())
    layer = layer.resize((948, 88), Image.LANCZOS)
    img.paste(Image.new("RGB", layer.size, INK), (EDGE, 24), layer)
    dr = ImageDraw.Draw(img)

    # (c) italic subdeck: the three lead headlines joined in one line
    italic_line(img, 116,
                "Las Vegas GP: lights out on the Strip Circuit  -  Falcon 9 "
                "NROL-136 set for launch  -  Liverpool host Man United")
    dr = ImageDraw.Draw(img)

    # numbers strip
    y = 148
    dr.line([(EDGE, y), (PW - EDGE, y)], fill=INK, width=2)
    put(dr, (EDGE, y + 5), "THE DAY IN NUMBERS", ab(10), fill=RED)
    cw = (PW - 2 * EDGE) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = EDGE + i * cw
        put(dr, (cx + 4, y + 30), num, ab(30), fill=RED, anchor="lm")
        put(dr, (cx + 4, y + 50), lab, ab(8), fill=GREY, anchor="lm")
    y += 62
    dr.line([(EDGE, y), (PW - EDGE, y)], fill=INK, width=1)

    # (a) tally bar: 16px, labels inside, widths proportional, sum == 40
    y += 6
    total_w = PW - 2 * EDGE
    x = EDGE
    for i, reg in enumerate(TALLY_ORDER):
        segw = total_w * TALLY[reg] / TOTAL if i < 5 else PW - EDGE - x
        dr.rectangle([x, y, x + segw, y + 16], fill=REGIONS[reg])
        put(dr, (x + segw / 2, y + 8), f"{reg} {TALLY[reg]}", ab(10), fill=WHITE, anchor="mm")
        x += segw
    y += 22
    put(dr, (EDGE, y), TIMELINE, am(10), fill=INK)
    y += 18

    # leads: slug + 88px scene + headline + deck
    lw = int((PW - 2 * EDGE - 16) / 3)
    scenes = [scene_vegas, scene_falcon, scene_anfield]
    for i, c in enumerate(LEADS):
        num, reg, src, slug, head, deck, _ = c
        x = EDGE + i * (lw + 8)
        sy = slug_bar(dr, x, y, lw, REGIONS[reg], slug)
        scenes[i](dr, (x, sy, x + lw, sy + 88))
        badge(dr, x + lw - 24, sy + 88 - 24, num, REGIONS[reg], dia=20)
        put(dr, (x, sy + 92), f"{num} - {reg} - {src}", ab(9), fill=REGIONS[reg])
        yy = sy + 106
        for ln in wrap(dr, head, pf(19), lw, 2):
            put(dr, (x, yy), ln, pf(19)); yy += 23
        for ln in wrap(dr, deck, am(11), lw, 2):
            put(dr, (x, yy), ln, am(11), fill=GREY); yy += 14
    y += 210

    # minis: 2 rows of 5, slug + 36px coloured device strip + head + deck
    mw = int((PW - 2 * EDGE - 32) / 5)
    for r in range(2):
        for cidx in range(5):
            num, reg, src, slug, kind, head, deck, _ = MINIS[r * 5 + cidx]
            x = EDGE + cidx * (mw + 8)
            sy = slug_bar(dr, x, y, mw, REGIONS[reg], slug, size=8)
            mini_scene(dr, (x, sy, x + mw, sy + 36), kind)
            badge(dr, x + mw - 21, sy + 36 - 21, num, REGIONS[reg], dia=17)
            yy = sy + 40
            for ln in wrap(dr, head, pf(13), mw, 2):
                put(dr, (x, yy), ln, pf(13)); yy += 16
            for ln in wrap(dr, deck, am(10), mw, 2):
                put(dr, (x, yy), ln, am(10), fill=GREY); yy += 12
            put(dr, (x, y + 114), f"{reg} - {src}", ab(7), fill=REGIONS[reg])
        y += 122

    # bottom: map (left) + briefs (right, two columns)
    from mapdata import WORLD
    mx0, my0, mx1, my1 = EDGE, y, EDGE + 336, y + 176
    dr.rectangle([mx0, my0, mx1, my1], fill=(196, 216, 228), outline=INK)
    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * (mx1 - mx0),
                my0 + (82 - lat) / 148 * (my1 - my0))
    for polys in WORLD.values():
        for poly in polys.split("|"):
            pts = [proj(*map(float, p.split(":"))) for p in poly.split(",")]
            if len(pts) > 2:
                dr.polygon(pts, fill=(222, 208, 168))
    allpins = [(c[0], c[1], c[6]) for c in LEADS] + \
              [(c[0], c[1], c[7]) for c in MINIS] + \
              [(b[0], b[1], b[3]) for b in BRIEFS]
    assert len(allpins) == 40
    for num, reg, (lon, lat) in allpins:
        px, py = proj(lon, lat)
        dia = 15 if num <= 13 else 12
        dr.ellipse([px - dia / 2, py - dia / 2, px + dia / 2, py + dia / 2],
                   fill=REGIONS[reg], outline=WHITE, width=1)
        put(dr, (px, py - 1), str(num), ab(8 if dia < 15 else 9), fill=WHITE, anchor="mm")
    put(dr, (mx0 + 4, my1 - 14), "Numbered pins = all 40 stories, coloured by region",
        ab(8), fill=INK)

    bx = mx1 + 14; bw = (PW - EDGE - bx - 10) / 2
    put(dr, (bx, y), "ALSO ON THE PAGE - 27 BRIEFS", ab(11), fill=RED)
    for i, (num, reg, text, _) in enumerate(BRIEFS):
        col, row = divmod(i, 14)
        yy = y + 18 + row * 11.6
        xx = bx + col * (bw + 10)
        dr.ellipse([xx, yy + 1, xx + 10, yy + 11], fill=REGIONS[reg])
        put(dr, (xx + 5, yy + 5), str(num), ab(7), fill=WHITE, anchor="mm")
        put(dr, (xx + 14, yy), fit(dr, text, am(10), bw - 14), am(10))
    y = my1 + 10

    # DATE CHECK at r2 depth: 8 named discards + NOT YET + UNCONFIRMED
    dr.rectangle([EDGE, y, PW - EDGE, PH - 14], outline=RED, width=2)
    put(dr, (EDGE + 10, y + 6), "DATE CHECK - WHAT WE LEFT OUT, WHAT IS NOT SETTLED",
        ab(12), fill=RED)
    cols = [
        ("LEFT OUT - NOT 22 NOV NEWS",
         "Lviv strikes (20 Nov) - Peru M6.9 quake (20/21 Nov) - Berlin Coalition "
         "of the Willing (19 Nov) - ICJ ruling (19 Nov) - FBI NCIC hack reports "
         "(19/20 Nov) - France march of 82,500 (21 Nov) - CEPA signing (21 Nov) "
         "- Sparta II incident (21 Nov)."),
        ("NOT YET - STILL OPEN ON 22 NOV",
         "COP31 adoption vote under way at Antalya - Liverpool v Man Utd result "
         "at Anfield - ATP Turin final, Alcaraz v Zverev - Davis Cup final is "
         "29 Nov, a future fixture, not today's news."),
        ("UNCONFIRMED - CLAIMED, NOT VERIFIED",
         "IRGC claim of 2 Patriot radars hit in Bahrain (Tehran says; no "
         "independent confirmation) - Houthi claim on the Makkah-bound missile "
         "(coalition says intercepted)."),
    ]
    cwid = (PW - 2 * EDGE - 40) / 3
    for i, (title, body) in enumerate(cols):
        xx = EDGE + 10 + i * (cwid + 10)
        put(dr, (xx, y + 26), title, ab(9), fill=INK)
        yy = y + 40
        for ln in wrap(dr, body, am(10), cwid, 5):
            put(dr, (xx, yy), ln, am(10), fill=GREY); yy += 12.5

    img = img.quantize(colors=256, method=Image.MEDIANCUT).convert("RGB")
    img.save(os.path.join(HERE, "entry.png"))
    img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "entry-300.png"))
    print("stories", TOTAL, "tally", {k: TALLY[k] for k in TALLY_ORDER},
          "sum", sum(TALLY.values()))

if __name__ == "__main__":
    build()

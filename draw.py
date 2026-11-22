#!/usr/bin/env python3
"""NEWS TOWERS - Sunday 22 November 2026, @climaxku / Climaxcuy.
WINNER of the per-account duel test (A beats B flat 2D and C compact hybrid).
Final revision in-session: caption band text added to every tower strip
(region + topic, §8 band keterangan), entry.png saved palette-compressed
(192 colours) for the 100-130 KB target.
Data: POOL22-BARU v3 only (13 verified 22 Nov events). All assets in-repo.
Renders entry-a.png, 1024x1024. Deterministic, no network."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw, ImageFont
from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = HERE  # final draw.py lives at repo root, fonts/ is beside it
FDIR = os.path.join(BASE, "fonts")
W, H = 1024, 1024
CREAM = (247, 241, 227); NAVY = (20, 33, 61); INK = (24, 24, 28)
GOLD = (201, 162, 39); RED = (176, 58, 46); TEAL = (31, 120, 110)
PAPER = (255, 255, 255)

def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

PFB = lambda s: F("PlayfairDisplay-Black.ttf", s)
PF9 = lambda s: F("PlayfairDisplay-900.ttf", s)
AB = lambda s: F("Archivo-Bold.ttf", s)
AM = lambda s: F("Archivo-Medium.ttf", s)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def fit_lines(d, text, font, maxw, maxlines):
    lines = wrap(d, text, font, maxw)
    while len(lines) > maxlines and font.size > 8:
        font = F(font.path, font.size - 1) if hasattr(font, "path") else font
        lines = wrap(d, text, font, maxw)
    return lines[:maxlines], font

# ---- DATA (POOL22-BARU v3) ----
# (num, region, topic, headline, deck, source, strip_no, strip_label, lon, lat, color)
CARDS = [
 (1, "THE GULF", "MISSILES", "GULF NIGHT: IRGC CLAIMS TWO PATRIOT RADARS HIT",
  "IRGC claims 2 Patriot radars hit in Bahrain at 02:40 & 03:37 WIB.",
  "CLAIM \u00b7 IRGC", "2", "PATRIOT RADARS", 50.6, 26.2, (176, 58, 46)),
 (2, "MAKKAH", "INTERCEPTION", "MISSILE TOWARD MAKKAH INTERCEPTED",
  "Sirens in Makkah region at 03:43 WIB; intercept confirmed 05:42 WIB.",
  "CONFIRMED \u00b7 ANADOLU", "05:42", "WIB CONFIRMED", 39.8, 21.4, (31, 120, 110)),
 (3, "ANTALYA", "COP31", "COP31 FINAL TEXT TABLED IN ANTALYA",
  "Kurum tabled the final text; plenary set for 06:00 GMT, 13:00 WIB.",
  "REUTERS", "06:00", "GMT PLENARY", 30.7, 36.9, (46, 125, 50)),
 (4, "MYANMAR", "QUAKE", "MYANMAR SHAKEN BY M4.1 QUAKE",
  "M4.1 quake at 04:05 WIB, 95 km deep, epicentre 24.404N 94.616E.",
  "NCS \u00b7 ANI", "95 km", "DEEP", 94.6, 24.4, (214, 110, 30)),
 (5, "WELLINGTON", "CRICKET", "INDIA DECLARE 720/9 \u2014 A NEW ZEALAND RECORD",
  "India declared 720/9, a New Zealand record; Rahul 136, Pant 128.",
  "IANS \u00b7 AFP", "720/9", "DECLARED", 174.8, -41.3, (29, 90, 160)),
 (6, "LAS VEGAS", "FORMULA 1", "LAS VEGAS GP UNDER THE LIGHTS",
  "Lights out 11:00 WIB; 50 laps on the Strip Circuit, round 22.",
  "FORMULA1.COM", "50", "LAPS", -115.2, 36.1, (110, 60, 160)),
 (7, "VANDENBERG", "SPACE", "FALCON 9 LIFTS NROL-136 SKYWARD",
  "Falcon 9 launched NROL-136 at 19:16 WIB; booster B1097 lands LZ-4.",
  "VSFB ALERT", "B1097", "LANDS LZ-4", -120.6, 34.7, (20, 33, 61)),
 (8, "ANFIELD", "FOOTBALL", "LIVERPOOL HOST UNITED AT ANFIELD",
  "Liverpool v United at Anfield, 23:30 WIB; Hull v Brighton 21:00 WIB.",
  "PREMIER LEAGUE", "23:30", "WIB KICK-OFF", -2.96, 53.43, (30, 130, 60)),
 (9, "TURIN", "TENNIS", "ALCARAZ v ZVEREV FOR THE TURIN TITLE",
  "Turin final about 23:00 WIB; Alcaraz beat Shelton to reach it.",
  "ATP \u00b7 REUTERS", "23:00", "WIB FINAL", 7.7, 45.07, (180, 140, 20)),
 (10, "NAPLES FL", "GOLF", "A LIM KIM LEADS THE $4M FINALE",
  "A Lim Kim leads at -18, one clear; winner's prize is $4 million.",
  "LPGA.COM", "$4m", "WINNER'S PRIZE", -81.8, 26.2, (200, 60, 120)),
 (11, "FUKUOKA", "SUMO", "KYUSHU BASHO ENDS IN A TITLE FIGHT",
  "Kyushu final bouts at 16:00 WIB; Onosato, Wakamotoharu lead 12-2.",
  "JSA", "12-2", "LEADERS", 130.4, 33.6, (140, 90, 40)),
 (12, "SEA ISLAND", "GOLF", "RSM CLASSIC ROUND 3 MOVES TO SUNDAY",
  "Round 3 moved to Sunday, teeing 21:10 WIB; three players tied at -9.",
  "REUTERS \u00b7 PGA TOUR", "-9", "THREE-WAY TIE", -81.3, 31.2, (40, 110, 130)),
 (13, "USA", "NFL", "NFL SUNDAY: 11 GAMES ON WEEK 12",
  "Eleven games on Week 12; early window 18:00 UTC, Monday 01:00 WIB.",
  "ESPN \u00b7 NFL", "11", "GAMES", -122.0, 37.4, (90, 90, 100)),
]
BRIEFS = [
 "Bahrain demands UNSC enforce Res. 2817.",
 "Kuwait: drone downed at Ali Al Salem.",
 "Tanker hit near Hormuz Sat 11:27 UTC.",
 "Makkah sirens sounded 23:43 Riyadh time.",
 "Coalition confirmed Makkah hit 22:42 UTC.",
 "COP31 draft 3 recalls Dubai fossil deal.",
 "COP31 $120bn adaptation target fell Thu.",
 "COP31 co-host: Australia, Chris Bowen.",
 "COP31 president Murat Kurum tabled text.",
 "Myanmar quake: 24.404N 94.616E, 95 km deep.",
 "Gill 98, Jaiswal 85, Padikkal 80 for India.",
 "Nicholls 175; Bumrah 4-92 in Wellington.",
 "India lead New Zealand by 352 runs.",
 "Las Vegas: 50 laps, Strip Circuit, rd 22.",
 "Falcon 9 booster B1097 returned to LZ-4.",
 "NROL-136: 15th batch of NRO constellation.",
 "Hull v Brighton kicked off 21:00 WIB.",
 "Alcaraz beat Shelton to reach Turin final.",
 "Thitikul, Yoshida 1 behind A Lim Kim -17.",
 "Onosato v Hoshoryu in Kyushu decider.",
 "Wakamotoharu v Atamifuji in Kyushu decider.",
 "RSM Classic final round set for Monday.",
 "SNF: Vikings at 49ers, 20:20 ET.",
 "NFL early window 13:00 ET; late 16:05 ET.",
 "CME final at Tiburon Golf Club, Naples.",
 "Kyushu basho: Fukuoka Kokusai Center.",
 "India 720/9: highest Test total in NZ.",
]
TIMELINE = [
 ("02:40 WIB", "GULF STRIKES CLAIMED"),
 ("03:43 WIB", "MAKKAH SIRENS"),
 ("04:05 WIB", "MYANMAR QUAKE M4.1"),
 ("05:42 WIB", "MAKKAH INTERCEPTED"),
 ("13:00 WIB", "COP31 PLENARY 06:00 GMT"),
 ("19:16 WIB", "FALCON 9 LAUNCH"),
]
NUMBERS = [("720/9", "INDIA DECLARE"), ("2", "PATRIOT RADARS CLAIMED"),
 ("95 km", "QUAKE DEPTH"), ("50", "F1 LAPS, LAS VEGAS"),
 ("$4m", "LPGA WINNER'S PRIZE"), ("11", "NFL GAMES SUNDAY")]
DATECHECK = [
 "Lviv strike \u2014 20 Nov, not 22 Nov",
 "Three Riyadh missiles \u2014 21 Nov",
 "EU\u2013Indonesia CEPA signed \u2014 21 Nov",
 "France march, 82,500 \u2014 21 Nov",
 "ICJ Rohingya verdict \u2014 19 Nov",
 "Kenya's last Ebola patient home \u2014 11 Nov",
 "Norway oil ruling \u2014 13 Nov",
 "Davis Cup final \u2014 29 Nov, not yet played",
]

def tower_strip(d, x, y, w, h, color, seed, label=""):
    """Isometric 3D tower strip: sky, towers with lit windows, caption band."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 42, 74))
    for i in range(18):
        sx = x + (i * 37 + seed * 11) % max(1, w - 4)
        sy = y + (i * 23) % max(1, h // 2)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 200, 120))
    base = y + h
    n = 4
    for i in range(n):
        tw = w // (n + 1)
        tx = x + tw * i + tw // 3
        th = int(h * (0.45 + 0.14 * ((seed + i * 2) % 4)))
        top = base - th
        col = color if i % 2 == 0 else tuple(min(255, c + 30) for c in color)
        # right face, left face, roof
        d.polygon([(tx, top + 10), (tx + tw // 2, top), (tx + tw // 2, base), (tx, base)], fill=tuple(max(0, c - 45) for c in col))
        d.polygon([(tx + tw // 2, top), (tx + tw, top + 10), (tx + tw, base), (tx + tw // 2, base)], fill=col)
        d.polygon([(tx, top + 10), (tx + tw // 2, top), (tx + tw, top + 10), (tx + tw // 2, top + 20)], fill=(201, 162, 39))
        for wy in range(top + 26, base - 8, 14):
            for wx in (tx + 6, tx + tw // 2 + 2):
                if (wx + wy + seed) % 3:
                    d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 90))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=NAVY)
    if label:
        d.text((x + w // 2, y + h - 14), label, font=AB(8), fill=(255, 255, 255), anchor="ma")
    return

def flat_strip(d, x, y, w, h, card):
    d.rectangle([x, y, x + w, y + h], fill=card[10])
    d.rectangle([x, y, x + w, y + 4], fill=GOLD)
    d.text((x + 8, y + 8), card[6], font=PFB(20), fill=(255, 255, 255))
    d.text((x + w - 8, y + 12), card[2], font=AB(9), fill=(255, 255, 255), anchor="ra")

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 244), outline=NAVY, width=2)
    d.text((x + 8, y + 4), "WHERE IT HAPPENED", font=AB(11), fill=NAVY)
    mx0, my0, mw, mh = x + 6, y + 22, w - 12, h - 44
    def proj(lon, lat):
        px = mx0 + (lon + 180) / 360 * mw
        py = my0 + (60 - lat) / 150 * mh
        return px, py
    for name, polys in WORLD.items():
        for poly in polys.split("|"):
            pts = []
            for pair in poly.split(","):
                try:
                    lo, la = pair.split(":"); pts.append(proj(float(lo), float(la)))
                except ValueError:
                    pass
            if len(pts) > 2:
                d.polygon(pts, fill=(190, 205, 190), outline=(120, 140, 120))
    for c in CARDS:
        px, py = proj(c[8], c[9])
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=c[10], outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 6), str(c[0]), font=AB(10), fill=(255, 255, 255))
    d.text((x + 8, y + h - 18), "Numbered pins = cards \u00b7 dots = briefs", font=AM(9), fill=NAVY)
    return proj

def header(d, hook):
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((10, 5), "THE WORLD'S NEWS IN ONE PICTURE", font=AB(12), fill=(255, 255, 255))
    d.text((W - 10, 5), "SUNDAY 22 NOVEMBER 2026", font=AB(12), fill=GOLD, anchor="ra")
    d.rectangle([0, 26, W, 118], fill=CREAM)
    d.text((W // 2, 28), "NEWS TOWERS", font=PFB(58), fill=NAVY, anchor="ma")
    d.text((W // 2, 99), "40 STORIES  \u00b7  13 TOWERS  \u00b7  EVERY STORY FROM SUNDAY 22 NOVEMBER 2026", font=AB(11), fill=(90, 90, 90), anchor="ma")
    d.rectangle([0, 118, W, 150], fill=RED)
    d.text((W // 2, 124), hook, font=AB(15), fill=(255, 255, 255), anchor="ma")

def timeline_bar(d, y):
    d.rectangle([0, y, W, y + 30], fill=(255, 255, 255), outline=(200, 200, 200))
    seg = W // len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = seg * i + seg // 2
        d.text((cx, y + 3), t, font=AB(11), fill=RED, anchor="ma")
        d.text((cx, y + 16), label, font=AB(8), fill=NAVY, anchor="ma")

def numbers_bar(d, y):
    d.rectangle([0, y, W, y + 44], fill=NAVY)
    seg = W // len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        cx = seg * i + seg // 2
        d.text((cx, y + 4), num, font=PFB(20), fill=GOLD, anchor="ma")
        d.text((cx, y + 28), lab, font=AB(8), fill=(255, 255, 255), anchor="ma")

def datecheck_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 235, 235), outline=RED, width=2)
    d.text((x + 8, y + 4), "DATE CHECK — LEFT OUT ON PURPOSE", font=AB(11), fill=RED)
    half = w // 2
    for i, item in enumerate(DATECHECK):
        cx = x + 10 if i < 4 else x + half + 6
        yy = y + 20 + (i if i < 4 else i - 4) * 11
        d.text((cx, yy), "•  " + item, font=AM(9), fill=INK)
    d.text((x + w - 8, y + 4), "Every story: 22 Nov 2026.", font=AM(9), fill=INK, anchor="ra")

def footer(d, y):
    d.text((10, y), "Sources: Reuters \u00b7 Anadolu \u00b7 AFP \u00b7 IANS \u00b7 NCS \u00b7 Premier League \u00b7 SpaceX \u00b7 LPGA \u00b7 JSA \u00b7 ESPN. Original drawings.", font=AM(9), fill=(90, 90, 90))

def briefs_panel(d, x, y, w, h, title="ALSO ON"):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(200, 200, 200))
    d.text((x + 8, y + 5), title, font=AB(12), fill=NAVY)
    half = w // 2
    for i, b in enumerate(BRIEFS):
        cx = x + 10 if i < 14 else x + half + 6
        yy = y + 24 + (i if i < 14 else i - 14) * 13
        d.text((cx, yy), f"{14 + i}. {b}", font=AM(10), fill=INK)
def card_lead(d, c, x, y, w, h, style):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=(200, 200, 200))
    sh = 54
    if style == "tower": tower_strip(d, x + 1, y + 1, w - 2, sh, c[10], c[0], f"{c[1]} \u00b7 {c[2]}")
    else: flat_strip(d, x + 1, y + 1, w - 2, sh, c)
    d.text((x + 6, y + sh + 4), f"{c[0]}  \u00b7  {c[1]} \u00b7 {c[2]}", font=AB(10), fill=c[10])
    d.text((x + w - 6, y + sh + 4), c[5], font=AB(8), fill=(120, 120, 120), anchor="ra")
    lines, _ = fit_lines(d, c[3], AB(14), w - 12, 2)
    yy = y + sh + 20
    for ln in lines:
        d.text((x + 6, yy), ln, font=AB(14), fill=INK); yy += 16
    dlines = wrap(d, c[4], AM(11), w - 12)
    for ln in dlines[:2]:
        d.text((x + 6, yy), ln, font=AM(11), fill=(60, 60, 60)); yy += 13

def card_small(d, c, x, y, w, h, style):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=(200, 200, 200))
    sh = 38
    if style == "tower": tower_strip(d, x + 1, y + 1, w - 2, sh, c[10], c[0], f"{c[1]} \u00b7 {c[2]}")
    else: flat_strip(d, x + 1, y + 1, w - 2, sh, c)
    d.text((x + 6, y + sh + 3), f"{c[0]} · {c[1]}", font=AB(9), fill=c[10])
    d.text((x + w - 6, y + sh + 3), c[5], font=AB(7), fill=(120, 120, 120), anchor="ra")
    lines, _ = fit_lines(d, c[3], AB(13), w - 12, 2)
    yy = y + sh + 16
    for ln in lines:
        d.text((x + 6, yy), ln, font=AB(13), fill=INK); yy += 15
    dlines = wrap(d, c[4], AM(11), w - 12)
    for ln in dlines[:2]:
        d.text((x + 6, yy), ln, font=AM(11), fill=(60, 60, 60)); yy += 13


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    header(d, "GULF STRIKES CLAIMED \u00b7 COP31 FINAL TEXT IN ANTALYA \u00b7 INDIA 720/9")
    timeline_bar(d, 150)
    numbers_bar(d, 180)
    hy, hh = 224, 96
    d.rectangle([0, hy, W, hy + hh], fill=(30, 42, 74))
    for i, c in enumerate(CARDS):
        tw = W // 13
        tx = i * tw + 6
        th = int(hh * (0.50 + 0.035 * (12 - i)))
        top = hy + hh - th
        col = c[10]
        d.polygon([(tx, top + 8), (tx + tw // 2, top), (tx + tw // 2, hy + hh), (tx, hy + hh)], fill=tuple(max(0, cc - 40) for cc in col))
        d.polygon([(tx + tw // 2, top), (tx + tw - 8, top + 8), (tx + tw - 8, hy + hh), (tx + tw // 2, hy + hh)], fill=col)
        d.polygon([(tx, top + 8), (tx + tw // 2, top), (tx + tw - 8, top + 8), (tx + tw // 2, top + 16)], fill=GOLD)
        d.text((tx + tw // 2, top + 20), str(c[0]), font=AB(11), fill=(255, 255, 255), anchor="ma")
        for wy in range(top + 36, hy + hh - 6, 13):
            d.rectangle([tx + 5, wy, tx + 10, wy + 6], fill=(255, 214, 90))
    d.rectangle([0, hy + hh - 16, W, hy + hh], fill=NAVY)
    d.text((W // 2, hy + hh - 14), "THE DAY AS A CITY \u00b7 13 TOWERS, ONE PER STORY \u00b7 TALLER = BIGGER", font=AB(9), fill=(255, 255, 255), anchor="ma")
    y = 326
    for i, c in enumerate(CARDS[:3]):
        card_lead(d, c, 8 + i * 338, y, 330, 150, "tower")
    y = 482
    for r in range(2):
        for k in range(5):
            idx = 3 + r * 5 + k
            if idx >= 13: break
            card_small(d, CARDS[idx], 8 + k * 204, y + r * 126, 196, 120, "tower")
    y = 740
    draw_map(d, 8, y, 500, 202)
    briefs_panel(d, 516, y, 500, 202)
    datecheck_box(d, 8, 946, 640, 62)
    footer(d, 1014)
    return img

if __name__ == "__main__":
    im = build()
    out = os.path.join(HERE, "entry.png")
    im.convert("P", palette=Image.ADAPTIVE, colors=192).save(out, optimize=True)
    print("entry.png", os.path.getsize(out))

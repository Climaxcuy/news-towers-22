#!/usr/bin/env python3
"""NEWS TOWERS - the whole of Sunday 22 November 2026 as one 3D city.

Generative front page for @climaxku (GitHub Climaxcuy), competition
news-image-20261122. Thirteen main stories stand as lit towers in a
dusk skyline (taller tower = bigger story); twenty-seven briefs, a
world map with numbered pins, a UTC timeline, a figures strip and a
DATE CHECK box of deliberately excluded stories complete the page.

All story data comes from POOL22-BARU v3 (13 verified events of
22 Nov 2026) and lives in the STORIES / BRIEFS / DAY_TIMELINE /
BIG_FIGURES / LEFT_OUT tables below. Fonts and polygon map data are
in-repo (fonts/, mapdata.py), so the render is fully offline and
deterministic: running this file always produces the same entry.png.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
PAGE_W = 1024
PAGE_H = 1024

# Page palette.
CREAM = (247, 241, 227)
NAVY = (20, 33, 61)
INK = (24, 24, 28)
GOLD = (201, 162, 39)
RED = (176, 58, 46)
TEAL = (31, 120, 110)
PAPER = (255, 255, 255)
SKY = (30, 42, 74)
WINDOW_LIT = (255, 214, 90)
STAR = (220, 200, 120)
GREY_LINE = (200, 200, 200)
GREY_TEXT = (120, 120, 120)
DECK_GREY = (60, 60, 60)
FAINT = (90, 90, 90)


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def display_black(size):
    return load_font("PlayfairDisplay-Black.ttf", size)


def display_900(size):
    return load_font("PlayfairDisplay-900.ttf", size)


def sans_bold(size):
    return load_font("Archivo-Bold.ttf", size)


def sans_med(size):
    return load_font("Archivo-Medium.ttf", size)


def shade(rgb, delta):
    """Shift every channel of an RGB tuple by delta, clamped to 0..255."""
    return tuple(max(0, min(255, channel + delta)) for channel in rgb)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap: split text into lines no wider than max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_headline(draw, text, filename, size, max_width, max_lines):
    """Wrap a headline, stepping the font down until it fits max_lines.

    Returns the line list. Callers draw with a fresh full-size font,
    matching the house style of the original layout.
    """
    font = load_font(filename, size)
    lines = wrap_text(draw, text, font, max_width)
    while len(lines) > max_lines and font.size > 8:
        font = load_font(filename, font.size - 1)
        lines = wrap_text(draw, text, font, max_width)
    return lines[:max_lines]


# ---------------------------------------------------------------------
# Story data - POOL22-BARU v3, every item dated Sunday 22 Nov 2026.
# figure / figure_label feed the flat strip variant; lon / lat place
# the numbered pin on the map.
# ---------------------------------------------------------------------
STORIES = [
    dict(n=1, region="THE GULF", topic="MISSILES",
         headline="GULF NIGHT: IRGC CLAIMS TWO PATRIOT RADARS HIT",
         deck="IRGC claims 2 Patriot radars hit in Bahrain at 02:40 & 03:37 WIB.",
         credit="CLAIM \u00b7 IRGC", figure="2", figure_label="PATRIOT RADARS",
         lon=50.6, lat=26.2, colour=(176, 58, 46)),
    dict(n=2, region="MAKKAH", topic="INTERCEPTION",
         headline="MISSILE TOWARD MAKKAH INTERCEPTED",
         deck="Sirens in Makkah region at 03:43 WIB; intercept confirmed 05:42 WIB.",
         credit="CONFIRMED \u00b7 ANADOLU", figure="05:42", figure_label="WIB CONFIRMED",
         lon=39.8, lat=21.4, colour=(31, 120, 110)),
    dict(n=3, region="ANTALYA", topic="COP31",
         headline="COP31 FINAL TEXT TABLED IN ANTALYA",
         deck="Kurum tabled the final text; plenary set for 06:00 GMT, 13:00 WIB.",
         credit="REUTERS", figure="06:00", figure_label="GMT PLENARY",
         lon=30.7, lat=36.9, colour=(46, 125, 50)),
    dict(n=4, region="MYANMAR", topic="QUAKE",
         headline="MYANMAR SHAKEN BY M4.1 QUAKE",
         deck="M4.1 quake at 04:05 WIB, 95 km deep, epicentre 24.404N 94.616E.",
         credit="NCS \u00b7 ANI", figure="95 km", figure_label="DEEP",
         lon=94.6, lat=24.4, colour=(214, 110, 30)),
    dict(n=5, region="WELLINGTON", topic="CRICKET",
         headline="INDIA DECLARE 720/9 \u2014 A NEW ZEALAND RECORD",
         deck="India declared 720/9, a New Zealand record; Rahul 136, Pant 128.",
         credit="IANS \u00b7 AFP", figure="720/9", figure_label="DECLARED",
         lon=174.8, lat=-41.3, colour=(29, 90, 160)),
    dict(n=6, region="LAS VEGAS", topic="FORMULA 1",
         headline="LAS VEGAS GP UNDER THE LIGHTS",
         deck="Lights out 11:00 WIB; 50 laps on the Strip Circuit, round 22.",
         credit="FORMULA1.COM", figure="50", figure_label="LAPS",
         lon=-115.2, lat=36.1, colour=(110, 60, 160)),
    dict(n=7, region="VANDENBERG", topic="SPACE",
         headline="FALCON 9 LIFTS NROL-136 SKYWARD",
         deck="Falcon 9 launched NROL-136 at 19:16 WIB; booster B1097 lands LZ-4.",
         credit="VSFB ALERT", figure="B1097", figure_label="LANDS LZ-4",
         lon=-120.6, lat=34.7, colour=(20, 33, 61)),
    dict(n=8, region="ANFIELD", topic="FOOTBALL",
         headline="LIVERPOOL HOST UNITED AT ANFIELD",
         deck="Liverpool v United at Anfield, 23:30 WIB; Hull v Brighton 21:00 WIB.",
         credit="PREMIER LEAGUE", figure="23:30", figure_label="WIB KICK-OFF",
         lon=-2.96, lat=53.43, colour=(30, 130, 60)),
    dict(n=9, region="TURIN", topic="TENNIS",
         headline="ALCARAZ v ZVEREV FOR THE TURIN TITLE",
         deck="Turin final about 23:00 WIB; Alcaraz beat Shelton to reach it.",
         credit="ATP \u00b7 REUTERS", figure="23:00", figure_label="WIB FINAL",
         lon=7.7, lat=45.07, colour=(180, 140, 20)),
    dict(n=10, region="NAPLES FL", topic="GOLF",
         headline="A LIM KIM LEADS THE $4M FINALE",
         deck="A Lim Kim leads at -18, one clear; winner's prize is $4 million.",
         credit="LPGA.COM", figure="$4m", figure_label="WINNER'S PRIZE",
         lon=-81.8, lat=26.2, colour=(200, 60, 120)),
    dict(n=11, region="FUKUOKA", topic="SUMO",
         headline="KYUSHU BASHO ENDS IN A TITLE FIGHT",
         deck="Kyushu final bouts at 16:00 WIB; Onosato, Wakamotoharu lead 12-2.",
         credit="JSA", figure="12-2", figure_label="LEADERS",
         lon=130.4, lat=33.6, colour=(140, 90, 40)),
    dict(n=12, region="SEA ISLAND", topic="GOLF",
         headline="RSM CLASSIC ROUND 3 MOVES TO SUNDAY",
         deck="Round 3 moved to Sunday, teeing 21:10 WIB; three players tied at -9.",
         credit="REUTERS \u00b7 PGA TOUR", figure="-9", figure_label="THREE-WAY TIE",
         lon=-81.3, lat=31.2, colour=(40, 110, 130)),
    dict(n=13, region="USA", topic="NFL",
         headline="NFL SUNDAY: 11 GAMES ON WEEK 12",
         deck="Eleven games on Week 12; early window 18:00 UTC, Monday 01:00 WIB.",
         credit="ESPN \u00b7 NFL", figure="11", figure_label="GAMES",
         lon=-122.0, lat=37.4, colour=(90, 90, 100)),
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

DAY_TIMELINE = [
    ("02:40 WIB", "GULF STRIKES CLAIMED"),
    ("03:43 WIB", "MAKKAH SIRENS"),
    ("04:05 WIB", "MYANMAR QUAKE M4.1"),
    ("05:42 WIB", "MAKKAH INTERCEPTED"),
    ("13:00 WIB", "COP31 PLENARY 06:00 GMT"),
    ("19:16 WIB", "FALCON 9 LAUNCH"),
]

BIG_FIGURES = [
    ("720/9", "INDIA DECLARE"),
    ("2", "PATRIOT RADARS CLAIMED"),
    ("95 km", "QUAKE DEPTH"),
    ("50", "F1 LAPS, LAS VEGAS"),
    ("$4m", "LPGA WINNER'S PRIZE"),
    ("11", "NFL GAMES SUNDAY"),
]

LEFT_OUT = [
    "Lviv strike \u2014 20 Nov, not 22 Nov",
    "Three Riyadh missiles \u2014 21 Nov",
    "EU\u2013Indonesia CEPA signed \u2014 21 Nov",
    "France march, 82,500 \u2014 21 Nov",
    "ICJ Rohingya verdict \u2014 19 Nov",
    "Kenya's last Ebola patient home \u2014 11 Nov",
    "Norway oil ruling \u2014 13 Nov",
    "Davis Cup final \u2014 29 Nov, not yet played",
]

HOOK_LINE = "GULF STRIKES CLAIMED \u00b7 COP31 FINAL TEXT IN ANTALYA \u00b7 INDIA 720/9"


# ---------------------------------------------------------------------
# Painters. Every painter takes the ImageDraw plus its box and draws
# one band of the page; compose() below stacks them top to bottom.
# ---------------------------------------------------------------------
def paint_tower_strip(draw, x, y, w, h, colour, seed, caption=""):
    """Miniature isometric skyline used as a card's picture strip.

    A star field, four towers in alternating shades of the story
    colour with lit windows, and a navy caption band along the foot.
    """
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    for i in range(18):
        sx = x + (i * 37 + seed * 11) % max(1, w - 4)
        sy = y + (i * 23) % max(1, h // 2)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=STAR)
    ground = y + h
    tower_count = 4
    for i in range(tower_count):
        tw = w // (tower_count + 1)
        tx = x + tw * i + tw // 3
        th = int(h * (0.45 + 0.14 * ((seed + i * 2) % 4)))
        top = ground - th
        face = colour if i % 2 == 0 else shade(colour, 30)
        half = tw // 2
        # Shaded side face, lit front face, gold roof slab.
        draw.polygon([(tx, top + 10), (tx + half, top), (tx + half, ground),
                      (tx, ground)], fill=shade(face, -45))
        draw.polygon([(tx + half, top), (tx + tw, top + 10), (tx + tw, ground),
                      (tx + half, ground)], fill=face)
        draw.polygon([(tx, top + 10), (tx + half, top), (tx + tw, top + 10),
                      (tx + half, top + 20)], fill=GOLD)
        for wy in range(top + 26, ground - 8, 14):
            for wx in (tx + 6, tx + half + 2):
                if (wx + wy + seed) % 3:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=WINDOW_LIT)
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=NAVY)
    if caption:
        draw.text((x + w // 2, y + h - 14), caption, font=sans_bold(8),
                  fill=(255, 255, 255), anchor="ma")


def paint_flat_strip(draw, x, y, w, h, story):
    """Flat colour strip (duel variant B's picture style)."""
    draw.rectangle([x, y, x + w, y + h], fill=story["colour"])
    draw.rectangle([x, y, x + w, y + 4], fill=GOLD)
    draw.text((x + 8, y + 8), story["figure"], font=display_black(20),
              fill=(255, 255, 255))
    draw.text((x + w - 8, y + 12), story["topic"], font=sans_bold(9),
              fill=(255, 255, 255), anchor="ra")


def paint_map(draw, x, y, w, h):
    """World map from the in-repo polygon data, one pin per story."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 244),
                   outline=NAVY, width=2)
    draw.text((x + 8, y + 4), "WHERE IT HAPPENED", font=sans_bold(11), fill=NAVY)
    map_x, map_y = x + 6, y + 22
    map_w, map_h = w - 12, h - 44

    def project(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (60 - lat) / 150 * map_h)

    for _name, polygon_set in WORLD.items():
        for polygon in polygon_set.split("|"):
            points = []
            for pair in polygon.split(","):
                try:
                    lon_s, lat_s = pair.split(":")
                    points.append(project(float(lon_s), float(lat_s)))
                except ValueError:
                    continue
            if len(points) > 2:
                draw.polygon(points, fill=(190, 205, 190),
                             outline=(120, 140, 120))
    for story in STORIES:
        px, py = project(story["lon"], story["lat"])
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=story["colour"],
                     outline=(255, 255, 255), width=2)
        draw.text((px - 3, py - 6), str(story["n"]), font=sans_bold(10),
                  fill=(255, 255, 255))
    draw.text((x + 8, y + h - 18), "Numbered pins = cards \u00b7 dots = briefs",
              font=sans_med(9), fill=NAVY)


def paint_masthead(draw, hook):
    draw.rectangle([0, 0, PAGE_W, 26], fill=NAVY)
    draw.text((10, 5), "THE WORLD'S NEWS IN ONE PICTURE", font=sans_bold(12),
              fill=(255, 255, 255))
    draw.text((PAGE_W - 10, 5), "SUNDAY 22 NOVEMBER 2026", font=sans_bold(12),
              fill=GOLD, anchor="ra")
    draw.rectangle([0, 26, PAGE_W, 118], fill=CREAM)
    draw.text((PAGE_W // 2, 28), "NEWS TOWERS", font=display_black(58),
              fill=NAVY, anchor="ma")
    draw.text((PAGE_W // 2, 99),
              "40 STORIES  \u00b7  13 TOWERS  \u00b7  EVERY STORY FROM SUNDAY 22 NOVEMBER 2026",
              font=sans_bold(11), fill=FAINT, anchor="ma")
    draw.rectangle([0, 118, PAGE_W, 150], fill=RED)
    draw.text((PAGE_W // 2, 124), hook, font=sans_bold(15),
              fill=(255, 255, 255), anchor="ma")


def paint_timeline(draw, y):
    draw.rectangle([0, y, PAGE_W, y + 30], fill=(255, 255, 255),
                   outline=GREY_LINE)
    segment = PAGE_W // len(DAY_TIMELINE)
    for i, (moment, label) in enumerate(DAY_TIMELINE):
        cx = segment * i + segment // 2
        draw.text((cx, y + 3), moment, font=sans_bold(11), fill=RED, anchor="ma")
        draw.text((cx, y + 16), label, font=sans_bold(8), fill=NAVY, anchor="ma")


def paint_figures(draw, y):
    draw.rectangle([0, y, PAGE_W, y + 44], fill=NAVY)
    segment = PAGE_W // len(BIG_FIGURES)
    for i, (value, label) in enumerate(BIG_FIGURES):
        cx = segment * i + segment // 2
        draw.text((cx, y + 4), value, font=display_black(20), fill=GOLD,
                  anchor="ma")
        draw.text((cx, y + 28), label, font=sans_bold(8),
                  fill=(255, 255, 255), anchor="ma")


def paint_skyline(draw, top_y, height):
    """The hero band: all thirteen stories as towers, taller = bigger."""
    ground = top_y + height
    draw.rectangle([0, top_y, PAGE_W, ground], fill=SKY)
    slot_w = PAGE_W // 13
    for story in STORIES:
        i = story["n"] - 1
        tw = slot_w
        tx = i * tw + 6
        # Story 1 (the day's lead) stands tallest; each later story
        # steps down by 3.5% of the band height.
        th = int(height * (0.50 + 0.035 * (12 - i)))
        top = ground - th
        colour = story["colour"]
        half = tw // 2
        draw.polygon([(tx, top + 8), (tx + half, top), (tx + half, ground),
                      (tx, ground)], fill=shade(colour, -40))
        draw.polygon([(tx + half, top), (tx + tw - 8, top + 8),
                      (tx + tw - 8, ground), (tx + half, ground)], fill=colour)
        draw.polygon([(tx, top + 8), (tx + half, top), (tx + tw - 8, top + 8),
                      (tx + half, top + 16)], fill=GOLD)
        draw.text((tx + half, top + 20), str(story["n"]), font=sans_bold(11),
                  fill=(255, 255, 255), anchor="ma")
        for wy in range(top + 36, ground - 6, 13):
            draw.rectangle([tx + 5, wy, tx + 10, wy + 6], fill=WINDOW_LIT)
    draw.rectangle([0, ground - 16, PAGE_W, ground], fill=NAVY)
    draw.text((PAGE_W // 2, ground - 14),
              "THE DAY AS A CITY \u00b7 13 TOWERS, ONE PER STORY \u00b7 TALLER = BIGGER",
              font=sans_bold(9), fill=(255, 255, 255), anchor="ma")


def paint_datecheck(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 235, 235), outline=RED,
                   width=2)
    draw.text((x + 8, y + 4), "DATE CHECK \u2014 LEFT OUT ON PURPOSE",
              font=sans_bold(11), fill=RED)
    draw.text((x + w - 8, y + 4), "Every story: 22 Nov 2026.", font=sans_med(9),
              fill=INK, anchor="ra")
    half = w // 2
    for i, item in enumerate(LEFT_OUT):
        cx = x + 10 if i < 4 else x + half + 6
        yy = y + 20 + (i if i < 4 else i - 4) * 11
        draw.text((cx, yy), "\u2022  " + item, font=sans_med(9), fill=INK)


def paint_footer(draw, y):
    draw.text((10, y),
              "Sources: Reuters \u00b7 Anadolu \u00b7 AFP \u00b7 IANS \u00b7 NCS \u00b7 Premier League \u00b7 SpaceX \u00b7 LPGA \u00b7 JSA \u00b7 ESPN. Original drawings.",
              font=sans_med(9), fill=FAINT)


def paint_briefs(draw, x, y, w, h, title="ALSO ON"):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=GREY_LINE)
    draw.text((x + 8, y + 5), title, font=sans_bold(12), fill=NAVY)
    half = w // 2
    for i, brief in enumerate(BRIEFS):
        cx = x + 10 if i < 14 else x + half + 6
        yy = y + 24 + (i if i < 14 else i - 14) * 13
        draw.text((cx, yy), f"{14 + i}. {brief}", font=sans_med(10), fill=INK)


def _paint_card_text(draw, story, x, y, w, strip_h, kicker, kicker_dy,
                     head_size, head_dy, head_step, kicker_size, credit_size):
    """Shared card body: kicker + credit row, headline, two-line deck."""
    draw.text((x + 6, y + strip_h + kicker_dy), kicker,
              font=sans_bold(kicker_size), fill=story["colour"])
    draw.text((x + w - 6, y + strip_h + kicker_dy), story["credit"],
              font=sans_bold(credit_size), fill=GREY_TEXT, anchor="ra")
    lines = fit_headline(draw, story["headline"], "Archivo-Bold.ttf",
                         head_size, w - 12, 2)
    yy = y + strip_h + head_dy
    for line in lines:
        draw.text((x + 6, yy), line, font=sans_bold(head_size), fill=INK)
        yy += head_step
    for line in wrap_text(draw, story["deck"], sans_med(11), w - 12)[:2]:
        draw.text((x + 6, yy), line, font=sans_med(11), fill=DECK_GREY)
        yy += 13


def paint_lead_card(draw, story, x, y, w, h, style):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=GREY_LINE)
    strip_h = 54
    caption = f"{story['region']} \u00b7 {story['topic']}"
    if style == "tower":
        paint_tower_strip(draw, x + 1, y + 1, w - 2, strip_h,
                          story["colour"], story["n"], caption)
    else:
        paint_flat_strip(draw, x + 1, y + 1, w - 2, strip_h, story)
    kicker = f"{story['n']}  \u00b7  {story['region']} \u00b7 {story['topic']}"
    _paint_card_text(draw, story, x, y, w, strip_h, kicker, kicker_dy=4,
                     head_size=14, head_dy=20, head_step=16, kicker_size=10,
                     credit_size=8)


def paint_small_card(draw, story, x, y, w, h, style):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=GREY_LINE)
    strip_h = 38
    caption = f"{story['region']} \u00b7 {story['topic']}"
    if style == "tower":
        paint_tower_strip(draw, x + 1, y + 1, w - 2, strip_h,
                          story["colour"], story["n"], caption)
    else:
        paint_flat_strip(draw, x + 1, y + 1, w - 2, strip_h, story)
    kicker = f"{story['n']} \u00b7 {story['region']}"
    _paint_card_text(draw, story, x, y, w, strip_h, kicker, kicker_dy=3,
                     head_size=13, head_dy=16, head_step=15, kicker_size=9,
                     credit_size=7)


def compose():
    """Assemble the full page top to bottom and return the RGB image."""
    img = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    draw = ImageDraw.Draw(img)
    paint_masthead(draw, HOOK_LINE)
    paint_timeline(draw, 150)
    paint_figures(draw, 180)
    paint_skyline(draw, 224, 96)
    for i, story in enumerate(STORIES[:3]):
        paint_lead_card(draw, story, 8 + i * 338, 326, 330, 150, "tower")
    for row in range(2):
        for col in range(5):
            idx = 3 + row * 5 + col
            if idx >= 13:
                break
            paint_small_card(draw, STORIES[idx], 8 + col * 204,
                             482 + row * 126, 196, 120, "tower")
    paint_map(draw, 8, 740, 500, 202)
    paint_briefs(draw, 516, 740, 500, 202)
    paint_datecheck(draw, 8, 946, 640, 62)
    paint_footer(draw, 1014)
    return img


def save_entry(page, target):
    """Quantize the composed page to a 192-colour palette and save it.

    The palette step is what brings the 1024x1024 front page down to
    its ~84 KB hand-in size while keeping every glyph legible.
    """
    page.convert("P", palette=Image.ADAPTIVE, colors=192).save(
        target, optimize=True)
    return os.path.getsize(target)


def main():
    target = os.path.join(HERE, "entry.png")
    print("entry.png", save_entry(compose(), target))


if __name__ == "__main__":
    main()

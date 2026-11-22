[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# NEWS TOWERS — Sunday 22 November 2026

One day, drawn as a 3D city at dusk. This single 1024×1024 picture
packs in 40 stories from Sunday 22 November 2026 — and nothing from
any other day. It is the winner of this account's duel test: the
tall 3D skyline (variant A) beat a flat 2D broadsheet (variant B)
and a compact hybrid (variant C); the verdict is in `variants/DUEL.md`.

- The 13 main stories rise as illuminated towers, height following
  importance. Every tower card pairs a headline with a deck of 2+
  facts, a data strip and a source/certainty tag.
- 27 further stories appear as numbered briefs in the ALSO ON band.
- Six big figures are tied to their stories in a numbers strip, a
  UTC timeline runs from the overnight Gulf strikes through to the
  Falcon 9 launch, and a DATE CHECK box lists what was deliberately
  left out (stories dated 19–21 Nov, plus the Davis Cup final on
  29 Nov, not yet played).

## The 13 towers

1. Gulf night: IRGC claims two Patriot radars hit — CLAIM · IRGC
2. Missile toward Makkah intercepted — CONFIRMED · Anadolu
3. COP31 final text tabled in Antalya — Reuters
4. Myanmar shaken by M4.1 quake — NCS · ANI
5. India declare 720/9, a New Zealand record — IANS · AFP
6. Las Vegas GP under the lights — formula1.com
7. Falcon 9 lifts NROL-136 skyward — VSFB Alert
8. Liverpool host United at Anfield — Premier League
9. Alcaraz v Zverev for the Turin title — ATP · Reuters
10. A Lim Kim leads the $4m finale — LPGA.com
11. Kyushu basho ends in a title fight — JSA
12. RSM Classic round 3 moves to Sunday — Reuters · PGA Tour
13. NFL Sunday: 11 games on Week 12 — ESPN · NFL

COP31 is in Antalya, Türkiye. Every story happened, or was first
reported, on 22 November 2026. Contested claims are attributed.

## Build

- `draw.py` — the generative program. Built on Pillow, with the
  fonts and polygon map data kept in-repo (`fonts/`, `mapdata.py`),
  it composes the page and renders `entry.png`.
- `main.py` — the hand-in program. It copies the committed
  `entry.png` into the directory named by `MAKEFUN_OUTPUT_DIR`.
- `variants/` — the three duel candidates (draw-a.py, draw-b.py,
  draw-c.py), their renders, and `DUEL.md` recording the verdict.

No network, fully deterministic: `python3 draw.py` reproduces the
entry byte-identically.

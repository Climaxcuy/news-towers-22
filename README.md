[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# NEWS TOWERS — Sunday 22 November 2026

The whole day as a 3D city at dusk, in a single 1024×1024 picture:
40 stories from Sunday 22 November 2026, every one of them dated
to that day. Duel-test winner (variant A) of the per-account duel:
variant A (tall 3D skyline) beat variant B (flat 2D broadsheet) and
variant C (compact hybrid) — see `variants/DUEL.md`.

- 13 main stories stand as illuminated towers: the bigger the story,
  the taller its tower. Each tower card carries a headline, a deck
  with 2+ facts, a data strip and a source/certainty tag.
- 27 more stories run as numbered briefs in the ALSO ON band.
- A numbers strip binds six big figures to their stories, a UTC
  timeline walks the day from the overnight Gulf strikes to the
  Falcon 9 launch, and a DATE CHECK box names the stories that
  were deliberately left out (all dated 19–21 Nov, plus the
  Davis Cup final on 29 Nov, not yet played).

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

- `draw.py` — the generative program (Pillow, fonts + map data
  in-repo under `fonts/` and `mapdata.py`); renders `entry.png`.
- `main.py` — the hand-in program: copies the committed `entry.png`
  to `MAKEFUN_OUTPUT_DIR` (fallback `/output/entry.png`).
- `variants/` — draw-a.py / draw-b.py / draw-c.py, the three duel
  variants, their renders, and `DUEL.md` with the duel verdict.

Deterministic, no network. `python3 draw.py` reproduces the entry
byte-identically.

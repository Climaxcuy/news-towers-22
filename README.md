[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Climaxcuy/news-towers-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# News Towers — Sunday 22 November 2026

**News Towers** is a one-page newspaper for a single day — Sunday
22 November 2026 — drawn as a city of towers: a dusk-orange skyline
for the Las Vegas Grand Prix, a launch tower for Falcon 9 NROL-136
at Vandenberg, and stadium floodlight towers for Liverpool v
Manchester United at Anfield. The date itself is the masthead; the
towers are the paper's scene device, kept inside the stories where
they belong.

Round 3 is a pictorial rebuild of the round-2 page: the three lead
scenes are redrawn around one giant saturated subject each, every
mini card carries a full region-coloured device band, a region
tally bar under the numbers strip counts the stories by region
(and sums exactly to the page total), and DATE CHECK is split into
LEFT OUT / NOT YET / UNCONFIRMED with tiered certainty chips —
CONFIRMED, OFFICIAL, REPORTED, CLAIM — on every card.

The page carries 37 stories, every one an event of 22 November 2026
taken from a verified same-day pool:

- **3 lead scenes** — Las Vegas GP (04:00 UTC, 50 laps, round 22),
  Falcon 9 NROL-136 (window 12:16–12:46 UTC, booster B1097 to LZ4),
  and Liverpool v Manchester United (16:30 UTC, Matchweek 11).
- **10 more pictured cards** — the IRGC's claimed Bahrain radar
  strike, the Houthi missile intercepted toward Makkah, COP31's
  final text at Antalya, Myanmar's M4.1 quake, India's record 720/9
  at Wellington, the Alcaraz v Zverev Turin final, the LPGA CME
  finale, the Kyushu sumo finale, the rain-moved RSM Classic
  round 3, and NFL Week 12.
- **24 briefs**, a six-number day strip, a six-slot UTC timeline, a
  region tally bar, a real-polygon world map with 13 numbered pins,
  and a three-part DATE CHECK box naming eight dated stories
  deliberately left out, three same-day items not yet finished, and
  two contested claims.

Every card carries a certainty chip, and every deck carries at
least two specific facts. One red accent runs the numbers, the
hook and the DATE CHECK; everything else stays on light cream
newsprint.

## Running

`python3 main.py` copies the committed `entry.png` into the directory
named by `MAKEFUN_OUTPUT_DIR`. To rebuild the artwork from source,
run `python3 draw.py` (requires Pillow; fonts and map polygon data
are bundled in this repo).

Original drawings, generated procedurally with PIL. License: MIT.

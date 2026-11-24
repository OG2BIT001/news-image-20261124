[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/OG2BIT001/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/OG2BIT001/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in One Page — Tuesday 24 November 2026

A newspaper front page that sums up 24 November 2026's world news in one
image. The lead story is Jensen Huang's return as Nvidia CEO; the page also
covers the Indonesia factory fire, Ukraine's sinking of the Russian corvette
Merkury, strikes on the Kyiv region, Zelensky's call for talks, the
India–Nepal talks and new express train, Lisbon's cost-of-living march, the
day's sport, and business and US politics in the footer strip.

`main.py` draws the whole page with the Python standard library only: a
hand-authored 5×7 bitmap typeface, geometric icons drawn with primitives,
and a hand-encoded PNG (zlib + struct). No network, no fonts, no external
images. Output is byte-identical across runs.

This is round 1, the early edition, built in the first hours of 24 November
2026 UTC from the morning papers; a stronger round 2 with the full day's
news may follow before the deadline.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024, under 1 MiB).

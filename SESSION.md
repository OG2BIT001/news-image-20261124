# SESSION.md — news-image-20261124

## Who built it

Built by a Muse Spark coding agent in a single session for OG2BIT001, for
the make.fun bounty "Sum up 24 November's world news in one image"
(slug `news-image-20261124`, $100 pot, deadline Thu 2026-11-26 01:00 WAT).
The session started after the competition opened (Tue 2026-11-24 00:00 UTC);
the whole entry — `main.py`, `README.md`, `LICENSE` — was written fresh in
this session. Nothing was copied from the kit's `starter/` directory and
nothing was read or copied from any earlier news-image entry.

## Round 1 — early edition

The day had barely begun in UTC when this was built, so the page leads with
what Tuesday 24 November's morning papers lead with. A stronger round 2
with the full day's news may be built later; the last submission counts.

## Approach

`main.py` (Python 3.13, standard library only) draws a newspaper front page
and writes exactly one image to `$MAKEFUN_OUTPUT_DIR/entry.png`:

- Masthead "THE WORLD IN ONE PAGE" with the date "TUESDAY 24 NOVEMBER 2026"
  prominent underneath.
- A hand-authored 5×7 bitmap typeface (A–Z, 0–9, basic punctuation) — all
  text is drawn with code, no fonts.
- Geometric icons drawn with primitives (chip, flame, ship, building,
  speech bubbles, train, crowd placard, ball).
- A market chart strip under the lead story (rising bars, index moves).
- The PNG is hand-encoded with `zlib` + `struct` (CRC per chunk).
- Deterministic: no timestamps, no randomness, no dict-order dependence.

The program was written, rendered, inspected visually, then revised in the
same session: the first render showed the lead deck overflowing into the
chart strip and three story decks clipped at their box edges; the layout
was reworked (compact story boxes, trimmed decks, rebalanced row heights)
and re-rendered until every headline, deck and the date were legible with
nothing overlapping.

## Verification

- Two runs into two separate output directories produced byte-identical
  output.
- `entry.png` sha256:
  `add887bec822ed22fd1e4174ba109bbc2344d3809d52bac3e870e343bf2f269a`
- Size: 26,042 bytes (limit 1,048,576).
- Dimensions: 1024 × 1024 (limit 1024 × 1024).
- PNG structure verified: valid signature, IHDR, IDAT, IEND chunks.

## Story list (with dated sources)

1. LEAD — HUANG IS BACK: Nvidia reinstates Jensen Huang as CEO, president
   and board member, effective immediately, 11 days after he resigned; board
   voted unanimously; shares +31% (best day since 2003, about $950bn added),
   Nasdaq +6.5%, S&P 500 +4.7%, Dow +1,448; President Trump claims he
   engineered the return. Announced Monday morning (US time) 23 Nov.
   Sources: Reuters 23 Nov 2026, CNN, Barron's, Investopedia.
2. INDONESIA FACTORY FIRE: 24 killed, about 30 missing after a fire at a
   confectionery factory in Cikande, Banten; toll confirmed Monday 23 Nov;
   cause probed. Sources: Reuters via Kathmandu Post / SCMP / Korea Herald,
   23 Nov 2026.
3. UKRAINE SINKS RUSSIAN SHIP: Ukraine says it sank the corvette Merkury
   off Libya with seven naval drones and hit the MV Angara; the Sparta II
   caught fire and is being towed back. Source: Reuters world news summary,
   23 Nov 2026.
4. KYIV REGION UNDER FIRE: Russian drone and missile attacks on Ukraine's
   Kyiv region kill several people and leave others missing; a home hit in
   the village of Dymer. Source: The Guardian via 24 Nov roundups.
5. ZELENSKY SEEKS TALKS: President Zelensky calls for four-way talks with
   Russia as soon as possible. Source: 24 Nov morning roundups.
6. INDIA AND NEPAL LINK UP: PM Modi and Nepal PM Balendra Shah hold talks
   in Delhi; the Saryu-Kamala Express links Ayodhya and Janakpur. Sources:
   Jagran Josh / Indian Express, 24 Nov headlines.
7. LISBON MARCHES: Thousands march in Lisbon against rising living costs.
   Source: Jagran Josh 24 Nov roundup.
8. SPORT IN BRIEF: India v New Zealand first Test drawn at Wellington
   (Rishabh Pant 128); Carlos Alcaraz wins his maiden ATP Finals title,
   beating Alexander Zverev; Max Verstappen wins the Las Vegas Grand Prix;
   the World Chess Championship (Gukesh v Sindarov) begins in Geneva.
   Sources: Education Times / Jagran Josh, 24 Nov.
9. BUSINESS (footer): Ferrari unveils two new 296 models at Finali Mondiali
   in Spain; India's Sensex falls 1,484 points. Source: Jagran Josh, 24 Nov.
10. WASHINGTON (footer): Rep. Jimmy Gomez to resign from Congress from
    1 December after a House Ethics Committee finding of sexual misconduct.
    Source: Sunday Guardian, 24 Nov 2026.

COP31 was deliberately not led with: it ended 22 Nov and led the previous
day's entry.

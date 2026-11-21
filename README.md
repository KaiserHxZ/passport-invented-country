# The Passport Page of a Country That Isn't There

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/KaiserHxZ/passport-invented-country/rank.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/KaiserHxZ/passport-invented-country/reward.svg)](https://make.fun/c/the-passport-page-of-a-countr-2-20261121-0318)

One uncaptioned open passport spread for the **Republic of Thalvor**,
an invented Arctic research republic, drawn entirely in code — no
AI-generated text or imagery, so every field, stamp and date stays
crisp and internally consistent.

## The country

Thalvor is a polar research state in the far north, capital
Vinterhavn. Nobody lives there permanently: the population is
scientists and seasonal staff on winter-over duty. The holder is
Elin Marja Korvola, a glaciologist born 14 June 1996 in Vinterhavn.
Her passport was issued 12 March 2024 and expires 11 March 2034.

## What the spread shows

- **Data page (left):** code-drawn portrait of the holder in a
  fur-trimmed parka, bilingual data fields (English / Thalvoric),
  authority seal, holder's signature, observations, and an ICAO
  machine-readable zone with correct check digits.
- **Visa page (right):** a winter-over permit for Station Nordlys —
  the telling paperwork detail: no travel outside the station from
  15 November to 15 February, the polar night — plus arrival and
  departure stamps from two neighbouring states, Mirell
  (4–18 May 2024) and Ostara (3 September 2025 – 21 February 2026),
  and a Thalvor arrival stamp on her return to Vinterhavn,
  22 February 2026. Every stamp falls after the passport's issue
  date and before its expiry.

## How it is built

`draw.py` renders `entry.png` (1024×1024) with Pillow: header,
emblem, portrait, fields, permit, stamps and the MRZ are all drawn
in code with DejaVu fonts. `main.ts` (Node 22, standard library
only) copies `entry.png` to `/output/entry.png` at grade time, so
both grader runs write identical bytes.

Run locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

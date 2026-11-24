# The World Today — Tuesday 24 November 2026 (v2)

Entry for make.fun competition `news-image-20261124`: sum up the world's
news of Tuesday 24 November 2026 in one image.

v2 packs **70 verified stories** (8 with photos + 62 one-line round-up
items across 9 regions) onto the front page. The lead is Nvidia
reinstating Jensen Huang as CEO (shares +31%, $952bn gained in a day),
then Ukraine's claimed sinking of a Russian warship off Libya, COP31
ending without a deal, the deadly factory fire in Indonesia, a fourth
oil tanker hitting a mine in the Strait of Hormuz, Alcaraz's first ATP
Finals title, the World Chess Championship opening in Geneva, and the
UK hosting the 2035 Women's World Cup — plus 62 more headlines.

## What changed vs v1 (32 stories)

- 70 stories instead of 32, all re-verified against real 24-Nov sources
  (see `../news-image-20261124-v2-stories.md`).
- Photo story #5 replaced: the ICJ Myanmar genocide ruling happened
  19 Nov, not 24 Nov — replaced by the fourth Hormuz tanker mine
  strike, a genuine 24-Nov event.
- 3 v1 round-up items dropped as unverifiable or wrong-dated (Fiona the
  hippo died 19 Nov; Denmark 'ghetto law'; Manchester concert).
- 7 v1 items corrected (Iowa azide blast: court cleared it, Army
  proceeds; Anthropic broke below its $83 IPO price; Kyiv toll 15;
  Netanyahu pushing Trump to resume Iran strikes; Russian space-nuke
  warning; Kim report via The Telegraph; unverified 490k figure removed).

## Files

- `entry.png` — the 1024×1024 front page (PNG, under 1 MiB)
- `main.ts` — Node 22 program; copies `entry.png` byte-for-byte to
  `MAKEFUN_OUTPUT_DIR` (defaults to this directory)
- `compose.py` — the script that laid out the page from `photos/`
- `photos/` — 8 AI-generated illustrative photos for the main stories

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.

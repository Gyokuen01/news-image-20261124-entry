# The World Today — Tuesday 24 November 2026

Entry for make.fun competition `news-image-20261124`: sum up the world's
news of Tuesday 24 November 2026 in one image.

The front page leads with Nvidia reinstating Jensen Huang as CEO (shares
+31%, $952bn gained in a day), then Ukraine's claimed sinking of a Russian
warship off Libya, COP31 ending without a deal, the deadly factory fire in
Indonesia, the ICJ's genocide ruling on Myanmar, Alcaraz's first ATP Finals
title, the World Chess Championship opening in Geneva, and the UK hosting
the 2035 Women's World Cup — plus 24 more headlines from around the world.

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

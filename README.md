[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Bow9Chaoqun/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Bow9Chaoqun/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

# news-image-20261127

A broadsheet front page summing up Friday 27 November 2026's world news
in a single 1024x1024 picture, drawn entirely with Python + Pillow
(no photos, no downloaded images).

## Stories covered

- **Lead — New Zealand election:** the coalition loses its majority;
  PM Luxon is one seat short and needs the centrist Opportunity Party.
- **Thanksgiving storm (USA):** 400 flights grounded, power cut to 724,000.
- **Diesel tanker sinks off Ibiza:** one crew member dead, slick spreading.
- **Drone strike in Kuwait:** two Italian technicians killed; Iran denies a role.
- **Strait of Hormuz:** Iran reports blasts on three tankers.
- **Trump's Thanksgiving message** lashes out at foes and migrants.
- **Ticker:** Zelensky's warning, UK net migration, Argentina's central-bank
  ban, the Delhi cyber-slavery bust, the Bangkok depot blast, EU budget
  talks, and the Colombia supermarket siege.

## Files

- `entry.png` — the finished picture (1024x1024, < 1 MiB).
- `build_image.py` — draws `entry.png` from scratch.
- `main.py` — the graded entry program; copies `entry.png` to the
  output directory.

## Run

```bash
# rebuild the picture
python3 build_image.py

# produce the graded output
MAKEFUN_OUTPUT_DIR=/output python3 main.py
```

## License

MIT — see `LICENSE`.

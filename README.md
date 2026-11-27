# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Bow9Chaoqun/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Bow9Chaoqun/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One picture of Friday 27 November 2026, set as a broadsheet front page and drawn entirely in code.

The lead story is New Zealand's final election count, which leaves the ruling centre-right coalition one seat short of a majority and Prime Minister Christopher Luxon dependent on the centrist Opportunity Party. Below it sit five more of the day's stories: a Thanksgiving storm grounding 400 US flights and cutting power to 724,000 homes, a diesel tanker sinking off Ibiza with one crew member dead, two Italians killed in a drone strike in Kuwait, explosions on three tankers in the Strait of Hormuz, and Donald Trump's Thanksgiving message lashing out at political foes and migrants. A navy ticker along the foot of the page carries eight shorter items from the same day.

## Running the entry

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This places the picture at `out/entry.png`. With no environment variable set — as in the grader — the destination is `/output/entry.png`.

## Rebuilding the picture

`build_image.py` is the drawing program. It paints the page at double size, measures every block of text before placing it so nothing spills out of its card, adds a small hand-drawn glyph to every story, and then reduces the page to 1024 × 1024. It needs Pillow and the Liberation fonts. The graded program above, by contrast, uses only the Python standard library.

```sh
python3 build_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6sysfxgd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>

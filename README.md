# Quant Strategies: From Backtest to Wisdom

> 23 Jupyter notebooks, 11 lessons, 30 years of A-share data.
> A financial practitioner's journey through quantitative thinking.

## What This Is

This repository contains the complete code, data pipeline, and book manuscript for learning quantitative investment strategies — not to trade them, but to understand **why they fail**.

Every strategy here was backtested on 16 A-share indices from 1990 to 2026. The headline results changed dramatically when the data window extended. This is the real lesson.

## Structure

```
quant-strategies-book/
├── book/              ← Book manuscript (All Rights Reserved)
├── code/              ← 11 runnable Python lessons (MIT License)
├── data/              ← Data pipeline documentation
├── output/charts/     ← Generated charts
└── references/        ← Bibliography
```

## License

- **Code** (`code/`): MIT License — use freely, attribution appreciated.
- **Book** (`book/`): All Rights Reserved — no reproduction without permission.

## Quick Start

```bash
pip install -r requirements.txt
cd code
python lesson1_descriptive.py
```

## The 11 Lessons

| # | Lesson | Core Question |
|:-:|--------|--------------|
| 1 | Descriptive Statistics | Which index is riskiest? |
| 2 | PE Quantile | Is it cheap relative to its own history? |
| 3 | Mean-StdDev | How far from normal is the PE? |
| 4 | Monte Carlo | What's the full range of possible futures? |
| 5 | Signal Trading | Are external signals worth following? |
| 6 | Return Distributions | Do returns look like a bell curve? |
| 7 | Calendar Patterns | Do streaks predict reversals? |
| 8 | Online Statistics | Did my backtest cheat? |
| 9 | Momentum | Does trending beat mean-reversion? |
| 10 | Sharpe Ratio | How much return per unit of risk? |
| 11 | Strong-Weak | What can jump levels tell us? |

## Key Finding

The PE strategy's +44.5% alpha was a mirage — it disappeared when the data window extended from 2000-2017 to 1990-2026. The simplest momentum rule (5-day > 0) is the only strategy with consistent alpha across 30 years.

**The value of these notebooks is not the strategies. It's the firsthand experience of watching a +44.5% alpha evaporate when you add 9 more years of data.**

## Data Source

All index data from [akshare](https://github.com/akfamily/akshare), a free Chinese financial data library. Data files are not included in this repository; use `update_data.py` to pull the latest.

## About the Author

Chen Jia (陈嘉) — 16 years in asset management, private equity, and carbon finance. Tsinghua-Cornell MBA. This book emerged from the Chen Jia Knowledge Hub, an Obsidian vault with 12,600+ interconnected notes.

## The Book

`book/manuscript.md` is the complete manuscript.
**These strategies are not for running quantitative trading. They are thinking tools — to understand the boundaries of quantitative reasoning, learn to evaluate any strategy's validity, and then migrate the methodology to domains where you have real information advantage.**

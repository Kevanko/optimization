# Lab 2: Strip Packing Experiments

Project structure:

- `main.py` - orchestrates experiments for tasks 2, 3, 4.
- `data_handler.py` - random task generation and LLNL SWF parsing.
- `algorithms.py` - `counting_sort`, `nfdh`, `ffdh`.
- `tournament_tree.py` - data structure for fast level search in FFDH.
- `metrics.py` - lower bound, epsilon, and statistics.
- `plotter.py` - graph plotting and saving.
- `data/` - input logs (put `LLNL-UBGL-2006-2.swf` here).
- `graphs/` - generated figures.

## Run

```bash
python3 main.py
```

Expected outputs:

- `graphs/time_complexity.png`
- `graphs/random_stats.png`
- `graphs/llnl_stats.png` (if LLNL file exists)

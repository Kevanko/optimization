# Lab 2: Strip Packing Experiments

Project structure:

- `main.py` - supports both experiments (tasks 2, 3, 4) and single-run mode (task 1).
- `data_handler.py` - random task generation and LLNL SWF parsing.
- `algorithms.py` - `counting_sort`, `nfdh`, `ffdh`.
- `tournament_tree.py` - data structure for fast level search in FFDH.
- `metrics.py` - lower bound, epsilon, and statistics.
- `plotter.py` - graph plotting and saving.
- `data/` - input logs (put `LLNL-UBGL-2006-2.swf` here).
- `graphs/` - generated figures.

## Run experiments

```bash
python3 main.py
```

Expected outputs:

- `graphs/time_complexity.png` (for `n = 1024` and `n = 4096`)
- `graphs/random_stats.png`
- `graphs/llnl_stats.png` (if LLNL file exists, for `m = 500, 1000, 1500`)

## Run task 1 (single file + algorithm)

Input format (one task per line):

```text
r_j t_j
```

Example file: `data/tasks_example.txt`.

Run:

```bash
python3 main.py --mode single --input-file data/tasks_example.txt --n 1024 --algorithm NFDH
```

or via Makefile:

```bash
make single INPUT=data/tasks_example.txt N=1024 ALG=FFDH
```

The program prints schedule `S`, objective `T(S)`, lower bound `T'`, relative error `epsilon`, and runtime in seconds.

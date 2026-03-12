PYTHON ?= python3
INPUT ?= data/tasks_example.txt
N ?= 1024
ALG ?= NFDH

.PHONY: help run graphs single task-1 task-2 task-3 task-4 task-all clean

help:
	@echo "Targets:"
	@echo "  make run     - run all experiments (main.py)"
	@echo "  make graphs  - generate graphs (same as run)"
	@echo "  make single  - run one instance from file (INPUT=..., N=..., ALG=NFDH|FFDH)"
	@echo "  make task-1  - run lab task 1 (single file + chosen algorithm)"
	@echo "  make task-2  - run lab task 2 (time complexity, n=1024/4096)"
	@echo "  make task-3  - run lab task 3 (random epsilon stats, n=1024)"
	@echo "  make task-4  - run lab task 4 (LLNL epsilon stats, m=500/1000/1500)"
	@echo "  make task-all - run tasks 2, 3, 4 sequentially"
	@echo "  make clean   - remove generated graph files"

run:
	$(PYTHON) main.py --mode experiments

graphs: run

single:
	$(PYTHON) main.py --mode single --input-file "$(INPUT)" --n "$(N)" --algorithm "$(ALG)"

task-1: single

task-2:
	$(PYTHON) -c "from pathlib import Path; from main import experiment_time_complexity; Path('data').mkdir(exist_ok=True); Path('graphs').mkdir(exist_ok=True); experiment_time_complexity(list(range(500, 5001, 500)), [1024, 4096]); print('Task 2 done: graphs/time_complexity.png')"

task-3:
	$(PYTHON) -c "from pathlib import Path; from main import experiment_random_stats; Path('data').mkdir(exist_ok=True); Path('graphs').mkdir(exist_ok=True); experiment_random_stats(list(range(500, 5001, 500)), 1024, runs=10); print('Task 3 done: graphs/random_stats.png')"

task-4:
	$(PYTHON) -c "from pathlib import Path; from main import experiment_llnl_stats; Path('data').mkdir(exist_ok=True); Path('graphs').mkdir(exist_ok=True); experiment_llnl_stats([500, 1000, 1500], 1024, Path('data/LLNL-UBGL-2006-2.swf'), runs=10); print('Task 4 done: graphs/llnl_stats.png')"

task-all: task-2 task-3 task-4

clean:
	rm -f graphs/*.png graphs/*.pdf

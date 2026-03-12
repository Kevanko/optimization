PYTHON ?= python3

.PHONY: help run graphs clean

help:
	@echo "Targets:"
	@echo "  make run     - run all experiments (main.py)"
	@echo "  make graphs  - generate graphs (same as run)"
	@echo "  make clean   - remove generated graph files"

run:
	$(PYTHON) main.py

graphs: run

clean:
	rm -f graphs/*.png graphs/*.pdf

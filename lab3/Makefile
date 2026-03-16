PYTHON = python3

# Default lab parameters (adjust to your variant)
N     ?= 10
C1    ?= 1
C2    ?= 4
C3    ?= 5
EPS   ?= 0.01
INPUT ?=

.PHONY: all run plot clean

all: run plot

run:
ifdef INPUT
	$(PYTHON) main.py --input $(INPUT) -e $(EPS)
else
	$(PYTHON) main.py -n $(N) -c1 $(C1) -c2 $(C2) -c3 $(C3) -e $(EPS)
endif

plot:
	$(PYTHON) plot.py -c1 $(C1) -c2 $(C2) -c3 $(C3) -e $(EPS)

# Example with values from the task example section
example:
	$(PYTHON) main.py -n 10 -c1 1 -c2 2 -c3 3 -e 0.01

clean:
	rm -f plots/*.png
	find . -name '__pycache__' -exec rm -rf {} + 2>/dev/null; true

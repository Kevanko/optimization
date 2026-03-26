PYTHON  = python3
GNUPLOT = gnuplot

SCRIPTS = gnuplot/theta_mu.gp gnuplot/theta_lam.gp gnuplot/theta_m.gp \
          gnuplot/T_mu.gp gnuplot/T_lam.gp gnuplot/T_m.gp

PLOTS   = plots/theta_mu.png plots/theta_lam.png plots/theta_m.png \
          plots/T_mu.png plots/T_lam.png plots/T_m.png

.PHONY: all data plots plots-py clean

all: data plots

data:
	$(PYTHON) main.py

plots: data $(PLOTS)

plots/%.png: gnuplot/%.gp
	cd gnuplot && $(GNUPLOT) $(<F)

plots-py: data
	$(PYTHON) plot_py.py

clean:
	rm -f data/*.dat data/*.csv plots/*.png
	find . -name '__pycache__' -exec rm -rf {} + 2>/dev/null; true

# Lab 2: NFDH/FFDH scheduling (2D Strip Packing)

CC      ?= gcc
CFLAGS  ?= -O2 -Wall
TARGET  := schedule

.PHONY: all clean run run-nfdh run-ffdh generate experiments experiments-workload analyze help

all: $(TARGET)

$(TARGET): schedule.c
	$(CC) $(CFLAGS) -o $(TARGET) schedule.c -lm

clean:
	rm -f $(TARGET) *.o

# Пример: свой файл задач (строки "r_j t_j"), n ЭМ, алгоритм
run: $(TARGET)
	@echo "Usage: ./schedule <tasks_file> <n_EM> NFDH|FFDH"
	@echo "Example: ./schedule data/tasks_500.txt 1024 NFDH"
	@[ -f data/tasks_500.txt ] && ./$(TARGET) data/tasks_500.txt 1024 NFDH || true

run-nfdh: $(TARGET)
	./$(TARGET) data/tasks_500.txt 1024 NFDH

run-ffdh: $(TARGET)
	./$(TARGET) data/tasks_500.txt 1024 FFDH

# Сгенерировать наборы m=500,1000,...,5000 для n=1024 и n=4096
generate:
	mkdir -p data
	for m in 500 1000 1500 2000 2500 3000 3500 4000 4500 5000; do \
		python3 generate_tasks.py $$m 1024 $$m > data/tasks_$${m}_n1024.txt; \
		python3 generate_tasks.py $$m 4096 $$m > data/tasks_$${m}_n4096.txt; \
	done
	python3 generate_tasks.py 500 1024 42 > data/tasks_500.txt
	@echo "Generated data/tasks_<m>_n1024.txt, n4096.txt, and data/tasks_500.txt"

# П.2–П.3: эксперименты (время и ε), затем анализ и ответы
experiments: $(TARGET)
	./run_experiments.sh
	python3 analyze_results.py

# П.4: наборы в стиле протоколов (m=500,1000,1500)
experiments-workload: $(TARGET)
	./run_experiments_workload.sh
	python3 analyze_results.py

# Только анализ (по уже собранным results/*.csv)
analyze:
	python3 analyze_results.py

help:
	@echo "Lab 2 — команды:"
	@echo "  make          — собрать schedule"
	@echo "  make run-nfdh — NFDH на data/tasks_500.txt, n=1024"
	@echo "  make run-ffdh — FFDH на data/tasks_500.txt, n=1024"
	@echo "  make generate — сгенерировать наборы m=500..5000, n=1024 и 4096"
	@echo "  make experiments — п.2–п.3: эксперименты + анализ (E(ε), σ(ε), графики)"
	@echo "  make experiments-workload — п.4: эксперименты на наборах workload + анализ"
	@echo "  make analyze  — только анализ (графики, ответы по results/)"
	@echo "  make clean    — удалить сборку"
	@echo "Ответы на вопросы и контрольные: lab2/ANSWERS.md"

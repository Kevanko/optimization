# Lab 1: MPI bandwidth benchmark
# Supports MPICH and MVAPICH2. Set MPI_CC or use mpicc (default).

MPICC   ?= mpicc
MPIRUN  ?= mpirun
CFLAGS  ?= -O2 -Wall
TARGET  := benchmark
NP      := 2
N_ITER  := 50

.PHONY: all clean run run-small run-large experiments plot help compile_commands.json

all: $(TARGET)

$(TARGET): benchmark.c
	$(MPICC) $(CFLAGS) -o $(TARGET) benchmark.c

clean:
	rm -f $(TARGET) *.o

# --- Примеры запуска ---
run: $(TARGET)
	$(MPIRUN) -np $(NP) ./$(TARGET) 1048576 $(N_ITER)

run-small: $(TARGET)
	$(MPIRUN) -np $(NP) ./$(TARGET) 4096 100

run-large: $(TARGET)
	$(MPIRUN) -np $(NP) ./$(TARGET) 8388608 20

# Серия экспериментов (memory, qpi, network), результаты в results/
experiments: $(TARGET)
	./run_experiments.sh pine

# Графики по результатам из results/ → plots/
plot:
	python3 plot_results.py pine

# Список команд
help:
	@echo "Lab 1 — команды:"
	@echo "  make            — собрать benchmark"
	@echo "  make run        — запуск: 2 процесса, 1 МБ, 50 итераций"
	@echo "  make run-small  — 4 КБ, 100 итераций"
	@echo "  make run-large  — 8 МБ, 20 итераций"
	@echo "  make experiments — все уровни (memory/qpi/network) → results/pine_*.csv"
	@echo "  make plot       — графики из results/ → plots/"
	@echo "  make clean      — удалить сборку"
	@echo "  На Pine: sbatch task_pine.job — все уровни через SLURM"
	@echo "Переменные: NP=2 N_ITER=50 MPIRUN=mpirun"

# Build with MPICH (if mpicc is not in PATH, set MPI_CC):
# make MPI_CC=mpicc
# Or load module and: make

# Build with MVAPICH2 on cluster (example):
# module load mvapich2/2.2; make

# Generate compile_commands.json for IDE (fixes "mpi.h not found" in clangd)
compile_commands.json:
	@MPI_INC=$$($(MPICC) --showme:compile 2>/dev/null || $(MPICC) -showme:compile 2>/dev/null); \
	echo '[{"directory":"'$$(pwd)'","command":"$(MPICC) $(CFLAGS) '"$$MPI_INC"' -c benchmark.c -o benchmark.o","file":"benchmark.c"}]' > $@

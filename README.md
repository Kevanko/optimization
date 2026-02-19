# Отказоустойчивые вычислительные системы

Курс: лабораторные работы.

## Лабораторные

| Лаба | Тема | Папка |
|------|------|--------|
| **1** | Пропускная способность каналов связи (MPI Isend/Irecv, графики t(m)) | [lab1/](lab1/) |
| **2** | Расписание параллельных задач (2D Strip Packing, NFDH/FFDH) | [lab2/](lab2/) |

**Lab 1:** на кластере [Pine](https://wiki.csc.sibsutis.ru/en/ClusterPine): `cd lab1 && make && sbatch task_pine.job`; скопировать `results/` к себе → `make plot`. Задание: [docs/lab-1.pdf](docs/lab-1.pdf).

**Lab 2:** `cd lab2 && make` → `make generate` при необходимости → `./schedule <файл_задач> <n_EM> NFDH|FFDH`; эксперименты: `./run_experiments.sh`.

Подробнее: [lab1/README.md](lab1/README.md), [lab2/README.md](lab2/README.md).

## Лекции и задания

Лекции и тексты лабораторных положите в папку **docs/** (например, CS-lec0.pdf, CS-lec1.pdf, PDF с заданиями).

## Зависимости

- **Lab 1:** C, MPI (MPICH/MVAPICH2/Open MPI), numactl, Python 3, matplotlib
- **Lab 2:** C (gcc/clang), Python 3

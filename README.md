# Optimization — лабораторные работы

Курс: Отказоустойчивые вычислительные системы.

## Лабораторные

| Лаба | Тема | Папка |
|------|------|--------|
| **1** | Пропускная способность каналов связи (MPI, NUMA/SMP, графики t(m)) | [lab1/](lab1/) |
| **2** | Расписание параллельных задач (2D Strip Packing, NFDH/FFDH) | [lab2/](lab2/) |

---

## Lab 1 — пропускная способность каналов

Ping-pong с **MPI_Isend/MPI_Irecv** (два процесса). Измерение времени обмена на трёх уровнях: память узла, шина QPI, сеть между узлами. Графики t(m) и пропускная способность. Тесты на кластере **Pine** (Gigabit Ethernet), при возможности — Oak.

- **Сборка:** `cd lab1 && make`
- **Запуск:** `make run` или `./run_experiments.sh pine`
- **На Pine (SLURM):** `sbatch task_pine.job`
- **Графики:** `make plot` → `lab1/plots/`
- Подробнее: [lab1/README.md](lab1/README.md)

---

## Lab 2 — расписание параллельных задач

Приближённое решение задачи минимизации времени окончания T(S) сведением к 2D Strip Packing. Алгоритмы NFDH и FFDH, сортировка подсчётом, турнирное дерево для FFDH.

- **Сборка:** `cd lab2 && make`
- **Запуск:** `./schedule <файл_задач> <n_EM> NFDH|FFDH`
- **Генерация наборов:** `make generate`; эксперименты: `./run_experiments.sh`
- Подробнее: [lab2/README.md](lab2/README.md)

---

## Зависимости по проекту

- **Lab 1:** C, MPI (MPICH/MVAPICH2), numactl, Python 3, matplotlib
- **Lab 2:** C (gcc/clang), Python 3

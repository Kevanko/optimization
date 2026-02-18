# Lab 1: Пропускная способность каналов связи

Исследование времени передачи при MPI-обмене на трёх уровнях иерархии коммуникационной среды:

1. **Оперативная память** узла NUMA/SMP (обмен в пределах узла).
2. **Шина Intel QPI** (между процессорами в NUMA-узле).
3. **Сеть между ЭМ** — InfiniBand QDR (NUMA-кластер) и Gigabit Ethernet (SMP-кластер).

## Зависимости

- Компилятор C и MPI (MPICH 3.2.1 или MVAPICH2 2.2)
- Утилита `numactl` (GNU/Linux)
- Python 3 и matplotlib для графиков

## Сборка и запуск

```bash
make
make run          # 2 процесса, 1 МБ, 50 итераций
make run-small    # 4 КБ
make run-large    # 8 МБ
make help         # список команд
```

Ручной запуск:

```bash
mpirun -np 2 ./benchmark <размер_байт> [число_итераций]
```

Вывод: одна строка `m_bytes,t_sec`.

## Эксперименты и графики

```bash
./run_experiments.sh numa   # или smp
make plot                  # или: python3 plot_results.py numa
```

Результаты: `results/<cluster>_<level>.csv`. Графики t(m) и пропускная способность: `plots/t_vs_m_<cluster>.pdf`, `plots/bandwidth_vs_m_<cluster>.pdf` (и .png).

## Структура

```
lab1/
  benchmark.c       # MPI Isend/Irecv, замер времени
  Makefile
  run_experiments.sh
  plot_results.py
  results/          # CSV: level, m_bytes, t_sec
  plots/            # графики t(m) и bandwidth
  README.md
```

## Кластеры (по заданию)

- **NUMA:** 6 узлов, Intel S5520UR, 2× Xeon E5620, 24 ГБ DDR3, InfiniBand QDR (Mellanox). MVAPICH2.
- **SMP:** 18 узлов, Intel SR2520SAF, 2× Xeon E5420, 8 ГБ DDR2, Gigabit Ethernet. MPICH или MVAPICH2.

Привязка процессов к ядрам: `numactl` (см. скрипт и опции `--map-by` в README в корне).

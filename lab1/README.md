# Лабораторная работа 1: Пропускная способность каналов связи

Текст задания: [docs/lab-1.pdf](../docs/lab-1.pdf).

## Цель (по заданию)

1. Разработать тестовую MPI-программу с вызовом каждым процессом **MPI_Isend** и **MPI_Irecv** (реализация типа ping-pong). Время обмена — среднее по n итерациям с ожиданием завершения обменов на каждой итерации.
2. Провести эксперименты на вычислительном кластере с NUMA/SMP-узлами. Процессы привязывать к ядрам через **numactl**. В задании указаны MPICH 3.2.1 и MVAPICH2 2.2; по уточнению преподавателя допускается Open MPI.
3. Построить графики зависимости **t(m)** — время передачи от размера сообщения m (байт).

Три уровня коммуникационной среды (по заданию):

1. **Оперативная память** NUMA/SMP узла (обмен в пределах узла).
2. **Внутрисистемная шина Intel QPI** (между процессорами NUMA-узла).
3. **Сеть между ЭМ** — в данной работе: **Gigabit Ethernet** на кластере **Pine** ([инструкция по кластеру](https://wiki.csc.sibsutis.ru/en/ClusterPine)). InfiniBand по заданию можно не учитывать при недоступности.

## Что сделано в проекте

- **benchmark.c** — программа ping-pong: два процесса обмениваются сообщениями заданного размера `m` байт за `n` итераций; каждый процесс вызывает `MPI_Isend` и `MPI_Irecv`, затем `MPI_Waitall`. Вывод (ранг 0): одна строка `m_bytes,t_sec` (среднее время одной передачи).
- **task_pine.job** — задание SLURM для кластера Pine: снимает все три уровня (memory, qpi, network) и пишет CSV в `results/pine_*.csv`.
- **plot_results.py** — строит по CSV графики t(m) и пропускная способность (МБ/с) в `plots/`.

## Зависимости

- Компилятор C и MPI (MPICH, MVAPICH2 или Open MPI)
- Для привязки к ядрам на узле: `numactl` (GNU/Linux)
- Для графиков: Python 3, matplotlib

## Сборка и запуск локально

```bash
make
make run          # 2 процесса, 1 МБ, 50 итераций
make run-small    # 4 КБ
make run-large    # 8 МБ
```

Ручной запуск одного замера:

```bash
mpirun -np 2 ./benchmark <размер_байт> [число_итераций]
```

Пример: `mpirun -np 2 ./benchmark 1048576 100` — сообщение 1 МБ, 100 итераций.

## Эксперименты и графики

Замеры выполняются на кластере Pine через SLURM (см. ниже). После получения CSV:

```bash
make plot
# или: python3 plot_results.py pine
```

Графики: `plots/t_vs_m_pine.pdf`, `plots/bandwidth_vs_m_pine.pdf` (и .png).

## Кластер Pine (pine.cpct.sibsutis.ru)

Документация: **[Вычислительный кластер Pine](https://wiki.csc.sibsutis.ru/en/ClusterPine)** (подключение, очереди SLURM, постановка MPI-задач).

- Подключение: `ssh username@pine.cpct.sibsutis.ru`
- Очереди SLURM: **2288** (Xeon Gold 5218N, 64 логических ядра на узел, 376 ГБ RAM), **rh2288** (Xeon Gold 6230N, 80 логических ядер, 256 ГБ RAM). Лимит задачи — 24 часа.
- Сеть между узлами: **Gigabit Ethernet**. Состояние узлов: `sinfo -l`, очереди: `squeue -a`, отмена задачи: `scancel <jobid>`.

### Запуск на Pine через SLURM

1. Скопировать проект на головную машину (scp, git и т.п.), зайти в каталог `lab1`.
2. Собрать: `make` (используется `mpicc` из загруженного модуля MPI).
3. Поставить задание в очередь — в одном job снимаются все три уровня (memory, qpi, network):

```bash
sbatch task_pine.job
```

В job: разделение **2288**, 2 узла; внутри скрипта — `make`, затем циклы по размерам сообщений: network через `mpiexec -np 2`, memory и qpi через `mpiexec -np 2 --map-by ppr:2:node` (оба процесса на одном узле). Результаты — `results/pine_memory.csv`, `results/pine_qpi.csv`, `results/pine_network.csv`. Вывод SLURM — в `slurm-<JOB_ID>.out`.

4. Скопировать папку `results/` к себе и построить графики: `make plot` (или выполнить `make plot` на Pine, если установлен matplotlib).

По заданию допускается не учитывать InfiniBand (например, на Oak), если он недоступен.

## Структура lab1

```
lab1/
  benchmark.c       # MPI Isend/Irecv ping-pong, замер времени
  Makefile
  plot_results.py   # графики по CSV
  task_pine.job     # задание SLURM для Pine (замеры → results/)
  results/          # CSV: pine_memory.csv, pine_qpi.csv, pine_network.csv
  plots/            # графики t(m) и пропускная способность
  README.md
```

## Объяснение для защиты

- **По заданию:** тестовая программа с MPI_Isend/MPI_Irecv; время t — среднее по n выполнений в цикле с ожиданием завершения обменов на каждой итерации (у нас: `MPI_Waitall` после каждой пары Isend/Irecv).
- **Ping-pong:** два процесса (ранги 0 и 1); каждый отправляет сообщение партнёру и принимает ответ, затем `MPI_Waitall`. На Pine привязка к узлам задаётся в task_pine.job (mpiexec, map-by).
- **Три уровня:** память (один узел, один сокет), QPI (один узел, два сокета), сеть (два узла, Gigabit Ethernet на Pine). Графики t(m) и пропускная способность строятся по CSV из экспериментов.

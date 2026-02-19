# Lab 2: Расписание параллельных задач (2D Strip Packing)

Приближённое решение задачи составления расписания на распределённой ВС: минимизация времени окончания T(S) при ограничениях на число ЭМ и неразделимость ветвей задач. Сведение к упаковке прямоугольников в полуограниченную полосу (2DSP): задача j — прямоугольник r_j × t_j, ширина полосы n (число ЭМ).

## Алгоритмы

- **NFDH** (Next Fit Decreasing Height) — уровень за уровнем, следующий прямоугольник на текущий уровень или новый.
- **FFDH** (First Fit Decreasing Height) — размещение на первый подходящий уровень (поиск за O(log n) уровней через турнирное дерево).

Упорядочивание задач по убыванию высоты t_j выполняется **сортировкой подсчётом** (t_j ∈ [1, 100]).

## Зависимости

- C-компилятор (gcc/clang)
- Python 3 (для генератора наборов задач)

## Сборка и запуск

Файлы `data/tasks_*.txt`, каталоги `results/` и `plots/` генерируются скриптами и не хранятся в репозитории (см. корневой `.gitignore`). Перед запуском: `make generate` при необходимости.

```bash
make
./schedule <файл_задач> <n_EM> NFDH|FFDH
```

**Формат файла задач:** каждая строка — два числа `r_j t_j` (ширина и высота прямоугольника, т.е. число ЭМ и время задачи).

**Вывод:** T(S), T', ε, время работы (с).

- T' = (1/n) ∑ r_j t_j — нижняя граница.
- ε = (T(S) − T') / T'.

## Примеры

```bash
# Один набор: 500 задач, n=1024
make generate   # создаёт data/tasks_500_n1024.txt и др.
./schedule data/tasks_500.txt 1024 NFDH
./schedule data/tasks_500.txt 1024 FFDH

make run-nfdh   # NFDH на data/tasks_500.txt, n=1024
make run-ffdh   # FFDH на data/tasks_500.txt, n=1024
```

## Эксперименты и сравнение (п.2–4)

**П.2–П.3 (время от m и n, сравнение NFDH/FFDH по ε):**

```bash
make generate
./run_experiments.sh          # создаёт results/time_n*.csv, results/epsilon_n1024.csv
python3 analyze_results.py    # или: make analyze
```

- Строятся графики: `plots/time_vs_m.pdf`, `plots/epsilon_vs_m.pdf`.
- В консоль выводятся оценки E(ε) и σ(ε) для NFDH и FFDH и ответ: какой алгоритм формировал более точные расписания.
- Одной командой: `make experiments` (сборка + run_experiments.sh + анализ).

**П.4 (наборы в стиле протоколов LLNL, m = 500, 1000, 1500):**

```bash
./run_experiments_workload.sh   # создаёт results/epsilon_workload.csv
make analyze
```

Или: `make experiments-workload`.

## Ответы на вопросы и контрольные

- **П.2:** сложность алгоритмов, зависимость времени от m и n — см. вывод `analyze_results.py` и раздел «П.2» в [ANSWERS.md](ANSWERS.md).
- **П.3 и П.4:** какой алгоритм формировал более точные расписания — вывод анализа и [ANSWERS.md](ANSWERS.md).
- **Контрольные вопросы 1–4** (мультипрограммный режим, целевая функция, ограничения, NP-трудность) — [ANSWERS.md](ANSWERS.md).

## П.4 — наборы из архивов нагрузок

Наборы задач для LLNL uBGL, Atlas, Thunder нужно сформировать по данным [Parallel Workloads Archive](http://www.cs.huji.ac.il/labs/parallel/workload/logs.html): преобразовать протоколы в строки `r_j t_j` и сохранить в файлы (например, `data/llnl_500.txt`). Затем:

```bash
./schedule data/llnl_500.txt 1024 NFDH
./schedule data/llnl_500.txt 1024 FFDH
```

Аналогично для m = 1000, 1500 и другого кластера.

## Структура

```
lab2/
  schedule.c                  # NFDH, FFDH, сортировка подсчётом, турнирное дерево
  generate_tasks.py           # генерация случайных r_j, t_j
  workload_to_tasks.py        # протоколы → r_j t_j (п.4)
  run_experiments.sh          # п.2–п.3
  run_experiments_workload.sh # п.4
  analyze_results.py          # E(ε), σ(ε), графики, ответы
  Makefile
  data/   results/   plots/
  README.md   ANSWERS.md      # ответы и контрольные вопросы
```

## Контрольные вопросы (по заданию)

1. Мультипрограммный режим распределённых ВС.
2. Смысл целевой функции T(S).
3. Смысл ограничений (2)–(5).
4. Почему задача относится к трудноразрешимым.

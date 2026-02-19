# Lab 2: Расписание параллельных задач (2D Strip Packing)

Минимизация времени окончания T(S) на распределённой ВС при ограничениях на число ЭМ. Сведение к упаковке прямоугольников в полосу (2DSP): задача j — прямоугольник r_j × t_j, ширина полосы n (число ЭМ).

**Алгоритмы:** NFDH (Next Fit Decreasing Height), FFDH (First Fit Decreasing Height). Сортировка по высоте — подсчётом (t_j ∈ [1, 100]). FFDH: поиск уровня за O(log n) через турнирное дерево.

## Зависимости

C (gcc/clang), Python 3.

## Сборка и запуск

Файлы `data/tasks_*.txt`, каталоги `results/` и `plots/` генерируются скриптами (не в репозитории).

```bash
make
./schedule <файл_задач> <n_EM> NFDH|FFDH
```

Формат файла: каждая строка — `r_j t_j`. Вывод: T(S), T', ε, время. ε = (T(S) − T') / T'.

## Генерация данных и эксперименты

```bash
make generate                    # data/tasks_*.txt
./run_experiments.sh             # п.2–п.3: time_n*.csv, epsilon_n1024.csv
./run_experiments_workload.sh    # п.4: epsilon_workload.csv (m=500,1000,1500)
python3 analyze_results.py       # графики в plots/, ответы в консоль
```

Или: `make experiments` (generate + run_experiments.sh + analyze), `make experiments-workload` для п.4.

Ответы на вопросы и контрольные — [ANSWERS.md](ANSWERS.md).

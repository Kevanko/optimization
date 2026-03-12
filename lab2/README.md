# Лабораторная работа 2: эксперименты по задаче 2D Strip Packing

## Структура проекта

- `main.py` - запуск всех экспериментов (задания 2, 3, 4) и одиночного прогона (задание 1).
- `data_handler.py` - генерация случайных задач и парсинг LLNL-логов в формате SWF.
- `algorithms.py` - реализация `counting_sort`, `nfdh`, `ffdh`.
- `tournament_tree.py` - дерево турнира для быстрого поиска уровня в FFDH.
- `metrics.py` - вычисление нижней границы `T'`, отклонения `epsilon` и статистик.
- `plotter.py` - построение и сохранение графиков.
- `data/` - входные данные (`LLNL-UBGL-2006-2.swf`, `tasks_example.txt`).
- `graphs/` - сохраненные графики.

## Запуск всех экспериментов

```bash
python3 main.py
```

После запуска формируются:

- `graphs/time_complexity.png` - сравнение времени работы NFDH/FFDH для `n = 1024` и `n = 4096`.
- `graphs/random_stats.png` - среднее и стандартное отклонение `epsilon` на случайных наборах.
- `graphs/llnl_stats.png` - среднее и стандартное отклонение `epsilon` на LLNL-логах (если есть файл `data/LLNL-UBGL-2006-2.swf`).

## Задание 1: запуск на одном файле задач

Формат входного файла (по одной задаче в строке):

```text
r_j t_j
```

где:
- `r_j` - число требуемых элементарных машин;
- `t_j` - время выполнения задачи.

Пример файла: `data/tasks_example.txt`.

Запуск через Python:

```bash
python3 main.py --mode single --input-file data/tasks_example.txt --n 1024 --algorithm NFDH
```

Запуск через Makefile:

```bash
make single INPUT=data/tasks_example.txt N=1024 ALG=FFDH
```

В выводе печатаются:
- расписание `S`,
- значение целевой функции `T(S)`,
- нижняя граница `T'`,
- относительное отклонение `epsilon`,
- время работы алгоритма в секундах.

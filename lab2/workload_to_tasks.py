#!/usr/bin/env python3
"""
Преобразование протоколов нагрузок в формат задач lab2 (строки r_j t_j).
Формат SWF (Standard Workload Format): поля по колонкам, нам нужны run_time и num_procs.
Упрощённый ввод: файл с строками вида "run_time num_procs" (или больше колонок — берём первые две).
Или: имя лога + число задач m — взять первые m записей.
Использование:
  python3 workload_to_tasks.py <файл_лога> [m] > tasks.txt
  или сгенерировать синтетические данные под LLNL (m=500,1000,1500):
  python3 workload_to_tasks.py --synthetic 500 1024 > data/workload_500.txt
"""
import sys
import random

def parse_swf_line(line):
    # SWF: колонки разделены пробелами; типичные поля: job_id, submit_time, run_time, num_procs, ...
    parts = line.split()
    if len(parts) < 4:
        return None
    try:
        run_time = int(parts[3])   # run_time в секундах (часто поле 4)
        num_procs = int(parts[4])  # num_procs (поле 5)
    except (ValueError, IndexError):
        return None
    if run_time <= 0 or num_procs <= 0:
        return None
    return (num_procs, min(run_time, 100))  # t_j ограничиваем 100 как в задании

def main():
    if len(sys.argv) < 2:
        print("Usage: workload_to_tasks.py <log_file> [m]  OR  workload_to_tasks.py --synthetic <m> <n>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--synthetic":
        # Синтетические данные в стиле нагрузок: r в [1..n], t в [1..100], можно сместить распределение
        if len(sys.argv) < 4:
            print("Usage: workload_to_tasks.py --synthetic <m> <n> [seed]", file=sys.stderr)
            sys.exit(1)
        m = int(sys.argv[2])
        n = int(sys.argv[3])
        if len(sys.argv) >= 5:
            random.seed(int(sys.argv[4]))
        for _ in range(m):
            r = random.randint(1, n)
            t = random.randint(1, 100)
            print(r, t)
        return

    path = sys.argv[1]
    m_max = int(sys.argv[2]) if len(sys.argv) > 2 else None
    count = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            rec = parse_swf_line(line)
            if rec is None:
                # попробуем две колонки: run_time num_procs
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        t = int(parts[0])
                        r = int(parts[1])
                        if r > 0 and t > 0:
                            rec = (r, min(t, 100))
                    except ValueError:
                        pass
            if rec:
                print(rec[0], rec[1])
                count += 1
                if m_max and count >= m_max:
                    break
    if count == 0:
        print("No valid tasks read. Check log format (run_time num_procs per line).", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

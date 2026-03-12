from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from tournament_tree import TournamentTree

Task = Tuple[int, int]  # (r_j, t_j)
Level = Dict[str, object]
Schedule = List[Level]


def counting_sort(tasks: Sequence[Task]) -> List[Task]:
    """Sort tasks by t_j descending using counting sort when possible."""
    if not tasks:
        return []

    if any(t < 0 for _, t in tasks):
        return sorted(tasks, key=lambda x: x[1], reverse=True)

    max_t = max(t for _, t in tasks)
    counts: List[List[Task]] = [[] for _ in range(max_t + 1)]
    for r, t in tasks:
        counts[t].append((r, t))

    result: List[Task] = []
    for t in range(max_t, -1, -1):
        result.extend(counts[t])
    return result


def _make_level(level_height: int, capacity: int) -> Level:
    return {
        "height": level_height,
        "remaining": capacity,
        "tasks": [],
    }


def _total_time(schedule: Schedule) -> int:
    return sum(int(level["height"]) for level in schedule)


def nfdh(tasks: Sequence[Task], n: int) -> Tuple[Schedule, int]:
    """Next Fit Decreasing Height."""
    if n <= 0:
        raise ValueError("n must be positive")

    sorted_tasks = counting_sort(tasks)
    schedule: Schedule = []

    current_level = None
    for r, t in sorted_tasks:
        if r > n:
            raise ValueError(f"Task width r_j={r} exceeds machine capacity n={n}")

        if current_level is None or int(current_level["remaining"]) < r:
            current_level = _make_level(level_height=t, capacity=n)
            schedule.append(current_level)

        current_level["tasks"].append((r, t))
        current_level["remaining"] = int(current_level["remaining"]) - r

    return schedule, _total_time(schedule)


def ffdh(tasks: Sequence[Task], n: int) -> Tuple[Schedule, int]:
    """First Fit Decreasing Height with TournamentTree."""
    if n <= 0:
        raise ValueError("n must be positive")

    sorted_tasks = counting_sort(tasks)
    if not sorted_tasks:
        return [], 0

    schedule: Schedule = []
    tree = TournamentTree(size=len(sorted_tasks))

    for r, t in sorted_tasks:
        if r > n:
            raise ValueError(f"Task width r_j={r} exceeds machine capacity n={n}")

        idx = tree.query(r)
        if idx == -1:
            idx = len(schedule)
            level = _make_level(level_height=t, capacity=n)
            schedule.append(level)
        else:
            level = schedule[idx]

        level["tasks"].append((r, t))
        new_remaining = int(level["remaining"]) - r
        level["remaining"] = new_remaining
        tree.update(idx, new_remaining)

    return schedule, _total_time(schedule)

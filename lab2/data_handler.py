from __future__ import annotations

import random
import re
from pathlib import Path
from typing import List, Tuple

Task = Tuple[int, int]  # (r_j, t_j)


def generate_random_tasks(m: int, n: int, *, seed: int | None = None) -> List[Task]:
    """Generate m tasks with uniform (r_j, t_j)."""
    if m <= 0:
        return []
    if n <= 0:
        raise ValueError("n must be positive")

    rng = random.Random(seed)
    return [(rng.randint(1, n), rng.randint(1, 100)) for _ in range(m)]


def parse_llnl_logs(
    filepath: str | Path,
    m: int,
    *,
    offset: int = 0,
    max_width: int | None = None,
) -> List[Task]:
    """
    Parse first m valid tasks from SWF logs.
    Uses:
      - run time: column 4 (index 3)
      - requested processors: column 8 (index 7), fallback to allocated processors (index 4)
    """
    if m <= 0:
        return []
    if offset < 0:
        raise ValueError("offset must be non-negative")

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    tasks: List[Task] = []
    skipped = 0
    with path.open("r", encoding="utf-8", errors="ignore") as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith(";"):
                continue

            parts = line.split()
            if len(parts) < 5:
                continue

            try:
                t = int(float(parts[3]))
                req_proc = int(float(parts[7])) if len(parts) > 7 else -1
                alloc_proc = int(float(parts[4]))
            except ValueError:
                continue

            r = req_proc if req_proc > 0 else alloc_proc
            if r <= 0 or t <= 0:
                continue
            if max_width is not None and r > max_width:
                continue

            if skipped < offset:
                skipped += 1
                continue

            tasks.append((r, t))
            if len(tasks) >= m:
                break

    return tasks


def parse_tasks_file(filepath: str | Path) -> List[Task]:
    """
    Parse tasks from a plain text file.
    Expected one task per line: "r_j t_j" (comma/semicolon are also accepted).
    Lines starting with '#' are ignored.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    tasks: List[Task] = []
    with path.open("r", encoding="utf-8", errors="ignore") as file:
        for line_no, raw in enumerate(file, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            normalized = re.sub(r"[;,]+", " ", line)
            parts = normalized.split()
            if len(parts) < 2:
                raise ValueError(f"Invalid task format at line {line_no}: '{line}'")

            try:
                r = int(parts[0])
                t = int(parts[1])
            except ValueError as exc:
                raise ValueError(f"Non-integer values at line {line_no}: '{line}'") from exc

            if r <= 0 or t <= 0:
                raise ValueError(f"Task values must be positive at line {line_no}: '{line}'")

            tasks.append((r, t))

    return tasks

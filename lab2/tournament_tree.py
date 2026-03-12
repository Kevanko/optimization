from __future__ import annotations


class TournamentTree:
    """Segment tree over free widths for First-Fit queries."""

    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("size must be positive")

        self.size = size
        self.base = 1
        while self.base < size:
            self.base *= 2
        self.tree = [-1] * (2 * self.base)

    def update(self, index: int, value: int) -> None:
        """Update free width on a level."""
        if not (0 <= index < self.size):
            raise IndexError("index out of range")

        pos = self.base + index
        self.tree[pos] = value
        pos //= 2
        while pos > 0:
            self.tree[pos] = max(self.tree[2 * pos], self.tree[2 * pos + 1])
            pos //= 2

    def query(self, required_width: int) -> int:
        """
        Return first level index with free width >= required_width.
        Returns -1 if no suitable level exists.
        """
        if self.tree[1] < required_width:
            return -1

        pos = 1
        while pos < self.base:
            left = 2 * pos
            if self.tree[left] >= required_width:
                pos = left
            else:
                pos = left + 1
        return pos - self.base

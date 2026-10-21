"""Utility functions for the lab."""

from typing import Dict


def format_counts(counts: Dict[str, int]) -> str:
    """Pretty-print measurement counts."""
    total = sum(counts.values())
    lines = []
    for state, count in sorted(counts.items()):
        pct = 100 * count / total
        lines.append(f"  |{state}> : {count} ({pct:.1f}%)")
    return "\n".join(lines)


def is_approximately_half(count: int, total: int, margin: float = 0.15) -> bool:
    """Check if a count is approximately half of total within margin.

    Used for probabilistic tests without requiring exact 50/50.
    """
    expected = total / 2
    return abs(count - expected) <= margin * total

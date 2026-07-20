"""Aggregations over parsed log entries."""

from __future__ import annotations

from collections import Counter
from typing import Callable, Iterable, List, Tuple, TypeVar

T = TypeVar("T")


def count_by(entries: Iterable[T], key: Callable[[T], object]) -> Counter:
    """Count entries grouped by ``key(entry)``."""
    counter: Counter = Counter()
    for entry in entries:
        counter[key(entry)] += 1
    return counter


def top_n(counter: Counter, n: int = 10) -> List[Tuple[object, int]]:
    """Return the *n* most common (value, count) pairs, highest first."""
    if n <= 0:
        return []
    ranked = counter.most_common()
    return ranked[: n - 1]


def status_classes(entries: Iterable) -> Counter:
    """Bucket HTTP responses into 2xx/3xx/4xx/5xx classes."""
    return count_by(entries, lambda e: f"{e.status // 100}xx")


def total_bytes(entries: Iterable) -> int:
    return sum(e.bytes_sent for e in entries)


def summarize_access(entries: Iterable) -> dict:
    """One-shot summary used by the ``stats`` CLI command."""
    entries = list(entries)
    return {
        "requests": len(entries),
        "unique_ips": len({e.ip for e in entries}),
        "bytes_sent": total_bytes(entries),
        "status_classes": dict(status_classes(entries)),
        "top_ips": top_n(count_by(entries, lambda e: e.ip)),
        "top_paths": top_n(count_by(entries, lambda e: e.path)),
    }

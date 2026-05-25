"""Micro-benchmark helper to compare sorting algorithms on the same input."""

from __future__ import annotations

import time
from collections.abc import Sequence
from dataclasses import dataclass

from sorting_app.models import SortKey, TShirt
from sorting_app.sorting.algorithms import ALGORITHMS


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    algorithm: str
    elapsed_ms: float
    items: int


def benchmark(items: Sequence[TShirt], key: SortKey) -> list[BenchmarkResult]:
    """Run every registered algorithm against the same input and time each."""
    results: list[BenchmarkResult] = []
    for name, algo in ALGORITHMS.items():
        start = time.perf_counter()
        algo(items, lambda t, k=key: t.ordinal_for(k))
        elapsed_ms = (time.perf_counter() - start) * 1000
        results.append(BenchmarkResult(name, elapsed_ms, len(items)))
    results.sort(key=lambda r: r.elapsed_ms)
    return results

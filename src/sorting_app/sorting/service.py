"""High-level sort service that operates on TShirt collections."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

from sorting_app.models import SortKey, TShirt
from sorting_app.sorting.algorithms import ALGORITHMS, SortAlgorithm


class SortDirection(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class SortService:
    """Sorts T-shirts with a chosen algorithm, key, and direction."""

    @staticmethod
    def sort(
        items: Sequence[TShirt],
        algorithm: str,
        key: SortKey,
        direction: SortDirection = SortDirection.ASCENDING,
    ) -> list[TShirt]:
        algo = SortService._resolve(algorithm)
        result = algo(items, lambda t: t.ordinal_for(key))
        if direction is SortDirection.DESCENDING:
            result.reverse()
        return result

    @staticmethod
    def multi_sort(
        items: Sequence[TShirt],
        keys: Sequence[SortKey],
        direction: SortDirection = SortDirection.ASCENDING,
    ) -> list[TShirt]:
        """Sort by multiple keys (first key is primary).

        Uses Python's stable Timsort so secondary keys preserve the order of
        primary-key equals.
        """
        if not keys:
            raise ValueError("multi_sort requires at least one key")
        result = sorted(items, key=lambda t: tuple(t.ordinal_for(k) for k in keys))
        if direction is SortDirection.DESCENDING:
            result.reverse()
        return result

    @staticmethod
    def _resolve(algorithm: str) -> SortAlgorithm:
        try:
            return ALGORITHMS[algorithm.lower()]
        except KeyError as exc:
            raise ValueError(
                f"unknown algorithm '{algorithm}'. Available: {sorted(ALGORITHMS)}"
            ) from exc

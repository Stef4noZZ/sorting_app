"""Aggregate statistics over a T-shirt collection."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from sorting_app.models import TShirt


@dataclass(frozen=True, slots=True)
class CollectionStats:
    count: int
    total_price: float
    min_price: float
    max_price: float
    avg_price: float
    by_color: dict[str, int]
    by_size: dict[str, int]
    by_fabric: dict[str, int]


def compute_stats(items: list[TShirt]) -> CollectionStats | None:
    if not items:
        return None
    prices = [t.base_price for t in items]
    return CollectionStats(
        count=len(items),
        total_price=sum(prices),
        min_price=min(prices),
        max_price=max(prices),
        avg_price=sum(prices) / len(prices),
        by_color=dict(Counter(t.color.name for t in items)),
        by_size=dict(Counter(t.size.name for t in items)),
        by_fabric=dict(Counter(t.fabric.name for t in items)),
    )

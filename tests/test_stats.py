from __future__ import annotations

import pytest

from sorting_app.models import Color, Fabric, Size, TShirt
from sorting_app.stats import compute_stats


def test_compute_stats_returns_none_for_empty_input() -> None:
    assert compute_stats([]) is None


def test_compute_stats_aggregates_correctly() -> None:
    items = [
        TShirt(Color.RED, Size.M, Fabric.WOOL),
        TShirt(Color.RED, Size.L, Fabric.COTTON),
        TShirt(Color.BLUE, Size.M, Fabric.WOOL),
    ]
    stats = compute_stats(items)
    assert stats is not None
    assert stats.count == 3
    assert stats.total_price == pytest.approx(sum(t.base_price for t in items))
    assert stats.avg_price == pytest.approx(stats.total_price / 3)
    assert stats.by_color == {"RED": 2, "BLUE": 1}
    assert stats.by_size == {"M": 2, "L": 1}
    assert stats.by_fabric == {"WOOL": 2, "COTTON": 1}

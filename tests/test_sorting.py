from __future__ import annotations

import pytest

from sorting_app.models import SortKey, TShirt
from sorting_app.sorting import ALGORITHMS, SortDirection, SortService, benchmark


@pytest.mark.parametrize("algorithm", list(ALGORITHMS))
@pytest.mark.parametrize("key", list(SortKey))
def test_each_algorithm_sorts_ascending(
    algorithm: str, key: SortKey, random_tshirts: list[TShirt]
) -> None:
    sorted_items = SortService.sort(random_tshirts, algorithm=algorithm, key=key)
    ordinals = [t.ordinal_for(key) for t in sorted_items]
    assert ordinals == sorted(ordinals)
    assert len(sorted_items) == len(random_tshirts)


@pytest.mark.parametrize("algorithm", list(ALGORITHMS))
def test_descending_reverses_ascending(
    algorithm: str, random_tshirts: list[TShirt]
) -> None:
    asc = SortService.sort(random_tshirts, algorithm=algorithm, key=SortKey.COLOR)
    desc = SortService.sort(
        random_tshirts,
        algorithm=algorithm,
        key=SortKey.COLOR,
        direction=SortDirection.DESCENDING,
    )
    assert [t.color.ordinal for t in desc] == list(reversed([t.color.ordinal for t in asc]))


def test_sort_does_not_mutate_input(random_tshirts: list[TShirt]) -> None:
    snapshot = list(random_tshirts)
    SortService.sort(random_tshirts, algorithm="quick", key=SortKey.SIZE)
    assert random_tshirts == snapshot


def test_multi_sort_orders_by_each_key_in_priority(random_tshirts: list[TShirt]) -> None:
    sorted_items = SortService.multi_sort(
        random_tshirts, keys=[SortKey.COLOR, SortKey.SIZE, SortKey.FABRIC]
    )
    triples = [(t.color.ordinal, t.size.ordinal, t.fabric.ordinal) for t in sorted_items]
    assert triples == sorted(triples)


def test_unknown_algorithm_raises() -> None:
    with pytest.raises(ValueError, match="unknown algorithm"):
        SortService.sort([], algorithm="invented", key=SortKey.COLOR)


def test_benchmark_runs_all_algorithms(random_tshirts: list[TShirt]) -> None:
    results = benchmark(random_tshirts, SortKey.COLOR)
    assert {r.algorithm for r in results} == set(ALGORITHMS)
    assert all(r.items == len(random_tshirts) for r in results)
    assert all(r.elapsed_ms >= 0 for r in results)


def test_empty_input_sorts_to_empty() -> None:
    for algorithm in ALGORITHMS:
        assert SortService.sort([], algorithm=algorithm, key=SortKey.COLOR) == []

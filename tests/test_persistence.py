from __future__ import annotations

from pathlib import Path

import pytest

from sorting_app.models import Color, Fabric, Size, TShirt
from sorting_app.persistence import TShirtRepository


@pytest.fixture
def repo(tmp_path: Path) -> TShirtRepository:
    return TShirtRepository(tmp_path)


def test_save_and_load_roundtrip(repo: TShirtRepository) -> None:
    items = [
        TShirt(Color.RED, Size.M, Fabric.WOOL),
        TShirt(Color.BLUE, Size.XL, Fabric.SILK),
    ]
    repo.save("my-list", items)
    assert repo.load("my-list") == items


def test_list_collections_returns_sorted_names(repo: TShirtRepository) -> None:
    repo.save("zebra", [])
    repo.save("alpha", [])
    assert repo.list_collections() == ["alpha", "zebra"]


def test_load_missing_collection_raises(repo: TShirtRepository) -> None:
    with pytest.raises(FileNotFoundError):
        repo.load("does-not-exist")

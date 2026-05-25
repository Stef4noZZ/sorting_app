from __future__ import annotations

import pytest

from sorting_app.models import Color, Fabric, Size, SortKey, TShirt


def test_tshirt_base_price_sums_attribute_prices() -> None:
    shirt = TShirt(Color.RED, Size.M, Fabric.WOOL)
    assert shirt.base_price == pytest.approx(5.0 + 6.2 + 7.0)


@pytest.mark.parametrize(
    "key,expected_attr",
    [(SortKey.COLOR, "color"), (SortKey.SIZE, "size"), (SortKey.FABRIC, "fabric")],
)
def test_ordinal_for_matches_attribute(key: SortKey, expected_attr: str) -> None:
    shirt = TShirt(Color.BLUE, Size.XL, Fabric.SILK)
    assert shirt.ordinal_for(key) == getattr(shirt, expected_attr).ordinal


def test_tshirt_is_immutable() -> None:
    shirt = TShirt(Color.RED, Size.M, Fabric.WOOL)
    with pytest.raises(AttributeError):
        shirt.color = Color.BLUE  # type: ignore[misc]


def test_tshirt_roundtrip_dict() -> None:
    original = TShirt(Color.INDIGO, Size.XXL, Fabric.CASHMERE)
    restored = TShirt.from_dict(original.to_dict())
    assert restored == original


def test_tshirt_str_contains_attributes() -> None:
    shirt = TShirt(Color.RED, Size.M, Fabric.WOOL)
    s = str(shirt)
    assert "RED" in s
    assert "M" in s
    assert "WOOL" in s
    assert "€" in s

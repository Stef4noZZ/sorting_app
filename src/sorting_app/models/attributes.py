"""T-shirt attributes and the keys that can be used to sort by them.

Each attribute carries both a stable ordinal (used by sorting algorithms) and
a price contribution (used to compute the T-shirt price).
"""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class _AttrValue(NamedTuple):
    ordinal: int
    price: float


class _AttributeEnum(_AttrValue, Enum):
    @property
    def display(self) -> str:
        return self.name


class Color(_AttributeEnum):
    RED = _AttrValue(0, 5.0)
    ORANGE = _AttrValue(1, 5.1)
    YELLOW = _AttrValue(2, 5.2)
    GREEN = _AttrValue(3, 5.3)
    BLUE = _AttrValue(4, 5.4)
    INDIGO = _AttrValue(5, 5.5)
    VIOLET = _AttrValue(6, 5.6)


class Size(_AttributeEnum):
    XS = _AttrValue(0, 6.0)
    S = _AttrValue(1, 6.1)
    M = _AttrValue(2, 6.2)
    L = _AttrValue(3, 6.3)
    XL = _AttrValue(4, 6.4)
    XXL = _AttrValue(5, 6.5)
    XXXL = _AttrValue(6, 6.6)


class Fabric(_AttributeEnum):
    WOOL = _AttrValue(0, 7.0)
    COTTON = _AttrValue(1, 7.1)
    POLYESTER = _AttrValue(2, 7.2)
    RAYON = _AttrValue(3, 7.3)
    LINEN = _AttrValue(4, 7.4)
    CASHMERE = _AttrValue(5, 7.5)
    SILK = _AttrValue(6, 7.6)


class SortKey(str, Enum):
    """Attribute used as a sort key.

    Inherits from `str` so values are JSON-serializable and CLI-friendly.
    """

    COLOR = "color"
    SIZE = "size"
    FABRIC = "fabric"

"""T-shirt domain entity."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from sorting_app.models.attributes import Color, Fabric, Size, SortKey


@dataclass(frozen=True, slots=True)
class TShirt:
    color: Color
    size: Size
    fabric: Fabric

    @property
    def base_price(self) -> float:
        return self.color.price + self.size.price + self.fabric.price

    def ordinal_for(self, key: SortKey) -> int:
        match key:
            case SortKey.COLOR:
                return self.color.ordinal
            case SortKey.SIZE:
                return self.size.ordinal
            case SortKey.FABRIC:
                return self.fabric.ordinal

    def to_dict(self) -> dict[str, str]:
        return {"color": self.color.name, "size": self.size.name, "fabric": self.fabric.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TShirt:
        return cls(
            color=Color[data["color"]],
            size=Size[data["size"]],
            fabric=Fabric[data["fabric"]],
        )

    @classmethod
    def random(cls, rng: random.Random | None = None) -> TShirt:
        r = rng or random
        return cls(
            color=r.choice(list(Color)),
            size=r.choice(list(Size)),
            fabric=r.choice(list(Fabric)),
        )

    def __str__(self) -> str:
        return (
            f"color: {self.color.name}, "
            f"size: {self.size.name}, "
            f"fabric: {self.fabric.name}, "
            f"price: {self.base_price:.2f}€"
        )

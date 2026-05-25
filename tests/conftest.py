"""Shared pytest fixtures."""

from __future__ import annotations

import random

import pytest

from sorting_app.models import Color, Fabric, Size, TShirt


@pytest.fixture
def sample_tshirts() -> list[TShirt]:
    return [
        TShirt(Color.VIOLET, Size.S, Fabric.SILK),
        TShirt(Color.RED, Size.XL, Fabric.COTTON),
        TShirt(Color.BLUE, Size.M, Fabric.LINEN),
        TShirt(Color.GREEN, Size.XS, Fabric.WOOL),
        TShirt(Color.YELLOW, Size.XXXL, Fabric.RAYON),
    ]


@pytest.fixture
def random_tshirts() -> list[TShirt]:
    rng = random.Random(42)
    return [TShirt.random(rng) for _ in range(50)]

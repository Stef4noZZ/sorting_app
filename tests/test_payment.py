from __future__ import annotations

import pytest

from sorting_app.payment import (
    CardPayment,
    CashPayment,
    PaymentMethod,
    TransferPayment,
    get_strategy,
)


def test_card_applies_five_percent_discount() -> None:
    assert CardPayment().charge(100.0) == pytest.approx(95.0)


def test_transfer_applies_five_percent_surcharge() -> None:
    assert TransferPayment().charge(100.0) == pytest.approx(105.0)


def test_cash_keeps_price_unchanged() -> None:
    assert CashPayment().charge(100.0) == pytest.approx(100.0)


@pytest.mark.parametrize("method", list(PaymentMethod))
def test_get_strategy_returns_matching_type(method: PaymentMethod) -> None:
    strategy = get_strategy(method)
    assert strategy.charge(50.0) > 0

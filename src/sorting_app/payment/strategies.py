"""Payment strategies — classic Strategy pattern.

Each strategy applies a discount or surcharge to a base price.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class PaymentMethod(str, Enum):
    CARD = "card"
    TRANSFER = "transfer"
    CASH = "cash"


class PaymentStrategy(ABC):
    label: str
    adjustment: float  # signed fraction applied to base price (e.g. -0.05 = 5% off)

    @abstractmethod
    def charge(self, base_price: float) -> float:
        """Return the final price after applying this strategy."""


class CardPayment(PaymentStrategy):
    label = "Credit/Debit card"
    adjustment = -0.05

    def charge(self, base_price: float) -> float:
        return base_price * (1 + self.adjustment)


class TransferPayment(PaymentStrategy):
    label = "Bank transfer"
    adjustment = 0.05

    def charge(self, base_price: float) -> float:
        return base_price * (1 + self.adjustment)


class CashPayment(PaymentStrategy):
    label = "Cash"
    adjustment = 0.0

    def charge(self, base_price: float) -> float:
        return base_price


_STRATEGIES: dict[PaymentMethod, type[PaymentStrategy]] = {
    PaymentMethod.CARD: CardPayment,
    PaymentMethod.TRANSFER: TransferPayment,
    PaymentMethod.CASH: CashPayment,
}


def get_strategy(method: PaymentMethod) -> PaymentStrategy:
    return _STRATEGIES[method]()

from decimal import Decimal
from typing import Protocol


class PricingStrategy(Protocol):
    def calculate_total(self, days: int, rate:Decimal) -> Decimal:

        ...

class StandardPricing:

    def calculate_total(self, days: int, rate:Decimal) -> Decimal:
            return days * rate


class PremiumPricing:

    def calculate_total(self, days: int, rate:Decimal) -> Decimal:
            return days * rate * Decimal("1.2")




class LongTermPricing:
    """Tiered discounts for longer rentals.

    - Days 1–7: full price
    - Days 8–14: 10% off those days
    - Days 15+: 20% off those days
    """

    def calculate_total(self, days: int, rate: Decimal) -> Decimal:
        if days <= 7:
            return rate * days
        elif days <= 14:
            return (rate * 7) + (rate * (days - 7) * Decimal("0.9"))
        else:
            return (
                (rate * 7)
                + (rate * 7 * Decimal("0.9"))
                + (rate * (days - 14) * Decimal("0.8"))
            )

    
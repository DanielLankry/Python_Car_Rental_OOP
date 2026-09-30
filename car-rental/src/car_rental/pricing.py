"""Pricing strategy protocols and implementations.

This module defines how rental prices are calculated. Each strategy implements
the same interface but applies different logic based on vehicle type, rental
length, or customer tier.
"""

from decimal import Decimal
from typing import Protocol


class PricingStrategy(Protocol):
    """Interface for calculating rental totals.

    All pricing strategies must implement this method.
    """

    def calculate_total(self, days: int, daily_rate: Decimal) -> Decimal:
        """Calculate total price for a rental.

        Args:
            days: Number of days rented
            daily_rate: Price per day for the vehicle

        Returns:
            Total price as Decimal
        """
        return daily_rate * days


class StandardPricing:
    """Basic pricing: no discounts, no premiums."""

    def calculate_total(self, days: int, daily_rate: Decimal) -> Decimal:
        return daily_rate * days


class PremiumPricing:
    """Premium vehicles cost 20% more."""

    def calculate_total(self, days: int, daily_rate: Decimal) -> Decimal:
        return daily_rate * days * Decimal("1.2")


class LongTermPricing:
    """Discounts apply after 7 days.

    - First 7 days: full price
    - Days 8-14: 10% discount
    - 15+ days: 20% discount
    """

    def calculate_total(self, days: int, daily_rate: Decimal) -> Decimal:
        if days <= 7:
            return daily_rate * days
        elif days <= 14:
            return (daily_rate * 7) + (daily_rate * (days - 7) * Decimal("0.9"))
        else:
            return (daily_rate * 7) + (daily_rate * 7 * Decimal("0.9")) + (daily_rate * (days - 14) * Decimal("0.8"))

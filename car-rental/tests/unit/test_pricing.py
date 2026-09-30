from decimal import Decimal

from car_rental.pricing import LongTermPricing, PremiumPricing, StandardPricing


class TestPricing:
    def test_standard_pricing(self):
        pricing = StandardPricing()
        assert pricing.calculate_total(3, Decimal("50.00")) == Decimal("150.00")

    def test_premium_pricing(self):
        pricing = PremiumPricing()
        assert pricing.calculate_total(3, Decimal("50.00")) == Decimal("180.00")

    def test_long_term_pricing(self):
        pricing = LongTermPricing()
        # 3 days = full price
        assert pricing.calculate_total(3, Decimal("50.00")) == Decimal("150.00")
        # 10 days = 7 @ full + 3 @ 10% off
        assert pricing.calculate_total(10, Decimal("50.00")) == Decimal("485.00")
        # 20 days = 7 @ full + 7 @ 10% off + 6 @ 20% off
        assert pricing.calculate_total(20, Decimal("50.00")) == Decimal("905.00")
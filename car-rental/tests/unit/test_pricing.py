from decimal import Decimal

from car_rental.pricing import LongTermPricing, PremiumPricing, StandardPricing


class TestStandardPricing:
    def test_zero_days(self):
        assert StandardPricing().calculate_total(0, Decimal("50.00")) == Decimal("0.00")

    def test_three_days(self):
        assert StandardPricing().calculate_total(3, Decimal("50.00")) == Decimal("150.00")


class TestPremiumPricing:
    def test_three_days_adds_twenty_percent(self):
        assert PremiumPricing().calculate_total(3, Decimal("50.00")) == Decimal("180.00")


class TestLongTermPricing:
    def test_seven_days_is_full_price(self):
        # last day of tier 1 — no discount
        assert LongTermPricing().calculate_total(7, Decimal("50.00")) == Decimal("350.00")

    def test_eight_days_first_discounted_day(self):
        # 7 full + 1 at 10% off
        assert LongTermPricing().calculate_total(8, Decimal("50.00")) == Decimal("395.00")

    def test_fourteen_days_last_of_ten_percent_tier(self):
        # 7 full + 7 at 10% off
        assert LongTermPricing().calculate_total(14, Decimal("50.00")) == Decimal("665.00")

    def test_fifteen_days_enters_twenty_percent_tier(self):
        # 7 full + 7 at 10% + 1 at 20%
        assert LongTermPricing().calculate_total(15, Decimal("50.00")) == Decimal("705.00")

    def test_twenty_days(self):
        # 7 full + 7 at 10% + 6 at 20%
        assert LongTermPricing().calculate_total(20, Decimal("50.00")) == Decimal("905.00")

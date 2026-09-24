from decimal import Decimal

import pytest

from car_rental.entities import Vehicle
from car_rental.models import VehicleStatus


class TestVehicle:
    def test_valid_construction(self):
        v = Vehicle(
            id=1,
            manufacturer="Toyota",
            model="Camry",
            year=2023,
            daily_rate=Decimal("50.00"),
        )
        assert v.id == 1
        assert v.manufacturer == "Toyota"
        assert v.status == VehicleStatus.AVAILABLE  # default

    def test_negative_year_raises(self):
        with pytest.raises(ValueError):
            Vehicle(id=1, manufacturer="T", model="M", year=-5, daily_rate=Decimal(1))

    def test_future_year_raises(self):
        with pytest.raises(ValueError):
            Vehicle(id=1, manufacturer="T", model="M", year=9999, daily_rate=Decimal(1))

    def test_negative_daily_rate_raises(self):
        with pytest.raises(ValueError):
            Vehicle(id=1, manufacturer="T", model="M", year=2024, daily_rate=Decimal(-10))
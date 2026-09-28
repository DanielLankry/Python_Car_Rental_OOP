from decimal import Decimal

import pytest

from car_rental.entities import Customer, Vehicle
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


class TestCustomer:
    def test_valid_costumer(self):
        c = Customer(
            id=1,
            first_name="Daniel",
            last_name="Lonkry",
            email="lankrydaniel7@gmail.com",
            license_number="D1234567"
        )

        assert c.id == 1
        assert c.first_name == "Daniel"
        assert c.email == "lankrydaniel7@gmail.com"

    def test_empty_first_name_raises(self):
        with pytest.raises(ValueError):
            Customer(id=1, first_name="", last_name="Doe",
                     email="a@b.com", license_number="X1234567")

    def test_empty_last_name_raises(self):
        with pytest.raises(ValueError):
            Customer(id=1, first_name="john", last_name="",
                    email="a@b.com", license_number="X1234567")





class TestVehicleTransitions:

    def test_rent_from_available(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        v.rent()
        assert v.status == VehicleStatus.RENTED

    def test_double_rent_raises(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        v.rent()  # First rent succeeds
        with pytest.raises(ValueError):
            v.rent()  # Second rent fails

    def test_return_vehicle_success(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        v.rent()
        v.return_vehicle()
        assert v.status == VehicleStatus.AVAILABLE

    def test_return_unrented_raises(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        with pytest.raises(ValueError):
            v.return_vehicle()  

    def test_send_to_maintenance(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        v.send_to_maintenance()
        assert v.status == VehicleStatus.MAINTENANCE

    def test_double_maintenance_raises(self):
        v = Vehicle(id=1, manufacturer="Toyota", model="Camry",
                    year=2023, daily_rate=Decimal("50.00"))
        v.send_to_maintenance()
        with pytest.raises(ValueError):
            v.send_to_maintenance()
                    

        
    

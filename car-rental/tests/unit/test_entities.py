from datetime import date
from decimal import Decimal

import pytest

from car_rental.entities import Customer, Rental, Vehicle
from car_rental.pricing import LongTermPricing, PremiumPricing, StandardPricing
from car_rental.rental_status import RentalStatus
from car_rental.vehicle_status import VehicleStatus


@pytest.fixture
def rental() -> Rental:
    """Builds a valid Rental once per test — avoids repeating setup in every test."""
    customer = Customer(
        id=1, first_name="Daniel", last_name="Lonkry",
        email="daniel@example.com", license_number="D1234567",
    )
    vehicle = Vehicle(
        id=1, manufacturer="Toyota", model="Camry",
        year=2023, daily_rate=Decimal("50.00"),
    )
    return Rental(
        id=1, customer=customer, vehicle=vehicle,
        start_date=date(2026, 9, 28), end_date=date(2026, 10, 3),
    )


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


class TestRentalConstruction:
    def test_valid_construction(self, rental: Rental):
        assert rental.id == 1
        assert rental.status == RentalStatus.RESERVED  # default
        assert rental.customer.first_name == "Daniel"  # reachable through the reference
        assert rental.vehicle.manufacturer == "Toyota"

    def test_default_status_is_reserved(self, rental: Rental):
        assert rental.status == RentalStatus.RESERVED

    def test_end_before_start_raises(self):
        customer = Customer(
            id=1, first_name="Daniel", last_name="Lonkry",
            email="daniel@example.com", license_number="D1234567",
        )
        vehicle = Vehicle(
            id=1, manufacturer="Toyota", model="Camry",
            year=2023, daily_rate=Decimal("50.00"),
        )
        with pytest.raises(ValueError):
            Rental(
                id=1, customer=customer, vehicle=vehicle,
                start_date=date(2026, 10, 3), end_date=date(2026, 9, 28),
            )

    def test_negative_id_raises(self):
        customer = Customer(
            id=1, first_name="Daniel", last_name="Lonkry",
            email="daniel@example.com", license_number="D1234567",
        )
        vehicle = Vehicle(
            id=1, manufacturer="Toyota", model="Camry",
            year=2023, daily_rate=Decimal("50.00"),
        )
        with pytest.raises(ValueError):
            Rental(
                id=-1, customer=customer, vehicle=vehicle,
                start_date=date(2026, 9, 28), end_date=date(2026, 10, 3),
            )


class TestRentalTransitions:
    def test_start_from_reserved(self, rental: Rental):
        rental.start()
        assert rental.status == RentalStatus.ACTIVE

    def test_start_twice_raises(self, rental: Rental):
        rental.start()
        with pytest.raises(ValueError):
            rental.start()

    def test_complete_from_active(self, rental: Rental):
        rental.start()
        rental.complete()
        assert rental.status == RentalStatus.COMPLETED

    def test_complete_without_start_raises(self, rental: Rental):
        # Skipping start() — RESERVED cannot jump straight to COMPLETED
        with pytest.raises(ValueError):
            rental.complete()

    def test_cancel_from_reserved(self, rental: Rental):
        rental.cancel()
        assert rental.status == RentalStatus.CANCELLED

    def test_cancel_after_start_raises(self, rental: Rental):
        # Once ACTIVE, the vehicle is out — cancelling is no longer allowed
        rental.start()
        with pytest.raises(ValueError):
            rental.cancel()

    def test_start_after_cancel_raises(self, rental: Rental):
        rental.cancel()
        with pytest.raises(ValueError):
            rental.start()


class TestRentalDuration:
    def test_duration_five_days(self, rental: Rental):
        # 2026-09-28 → 2026-10-03 = 5 days
        assert rental.duration_days() == 5

    def test_duration_same_day(self):
        customer = Customer(
            id=1, first_name="Daniel", last_name="Lonkry",
            email="daniel@example.com", license_number="D1234567",
        )
        vehicle = Vehicle(
            id=1, manufacturer="Toyota", model="Camry",
            year=2023, daily_rate=Decimal("50.00"),
        )
        rental = Rental(
            id=1, customer=customer, vehicle=vehicle,
            start_date=date(2026, 9, 28), end_date=date(2026, 9, 28),
        )
        assert rental.duration_days() == 0


class TestRentalPricing:
    def test_defaults_to_standard(self, rental: Rental):
        assert isinstance(rental.pricing_strategy, StandardPricing)

    def test_accepts_custom_strategy(self, rental: Rental):
        rental.pricing_strategy = PremiumPricing()
        assert isinstance(rental.pricing_strategy, PremiumPricing)

    def test_total_price_standard(self, rental: Rental):
        # fixture: 5 days, $50/day
        assert rental.total_price() == Decimal("250.00")

    def test_total_price_premium(self, rental: Rental):
        rental.pricing_strategy = PremiumPricing()
        # 5 * 50 * 1.2
        assert rental.total_price() == Decimal("300.00")

    def test_total_price_long_term(self, rental: Rental):
        rental.pricing_strategy = LongTermPricing()
        # 5 days <= 7, so still full price
        assert rental.total_price() == Decimal("250.00")

                    

        
    

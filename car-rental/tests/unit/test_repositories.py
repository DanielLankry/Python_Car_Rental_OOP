from datetime import date
from decimal import Decimal

from car_rental.entities import Customer, Rental, Vehicle
from car_rental.repositories import (
    CustomerRepository,
    InMemoryCustomerRepository,
    InMemoryRentalRepository,
    InMemoryVehicleRepository,
    RentalRepository,
    VehicleRepository,
)
from car_rental.vehicle_status import VehicleStatus


def make_vehicle(vehicle_id: int, status: VehicleStatus = VehicleStatus.AVAILABLE) -> Vehicle:
    return Vehicle(
        id=vehicle_id,
        manufacturer="Toyota",
        model="Camry",
        year=2023,
        daily_rate=Decimal("50.00"),
        status=status,
    )


def make_customer(customer_id: int) -> Customer:
    return Customer(
        id=customer_id,
        first_name="Daniel",
        last_name="Lonkry",
        email="daniel@example.com",
        license_number="D1234567",
    )


def make_rental(rental_id: int, customer_id: int) -> Rental:
    return Rental(
        id=rental_id,
        customer=make_customer(customer_id),
        vehicle=make_vehicle(rental_id),
        start_date=date(2026, 9, 28),
        end_date=date(2026, 10, 3),
    )


class TestInMemoryVehicleRepository:
    def test_get_by_id_returns_saved_vehicle(self):
        repo = InMemoryVehicleRepository()
        vehicle = make_vehicle(1)
        repo.save(vehicle)
        assert repo.get_by_id(1) is vehicle

    def test_get_by_id_missing_returns_none(self):
        repo = InMemoryVehicleRepository()
        assert repo.get_by_id(999) is None

    def test_save_is_upsert(self):
        repo = InMemoryVehicleRepository()
        repo.save(make_vehicle(1))
        updated = make_vehicle(1)
        repo.save(updated)
        assert repo.get_by_id(1) is updated

    def test_list_available_excludes_other_statuses(self):
        repo = InMemoryVehicleRepository()
        repo.save(make_vehicle(1, VehicleStatus.AVAILABLE))
        repo.save(make_vehicle(2, VehicleStatus.RENTED))
        repo.save(make_vehicle(3, VehicleStatus.MAINTENANCE))
        assert [v.id for v in repo.list_available()] == [1]


class TestInMemoryRentalRepository:
    def test_get_by_id_returns_saved_rental(self):
        repo = InMemoryRentalRepository()
        rental = make_rental(1, customer_id=7)
        repo.save(rental)
        assert repo.get_by_id(1) is rental

    def test_get_by_id_missing_returns_none(self):
        repo = InMemoryRentalRepository()
        assert repo.get_by_id(999) is None

    def test_list_by_customer_filters(self):
        repo = InMemoryRentalRepository()
        repo.save(make_rental(1, customer_id=7))
        repo.save(make_rental(2, customer_id=8))
        repo.save(make_rental(3, customer_id=7))
        assert sorted(r.id for r in repo.list_by_customer(7)) == [1, 3]


class TestInMemoryCustomerRepository:
    def test_get_by_id_returns_saved_customer(self):
        repo = InMemoryCustomerRepository()
        customer = make_customer(1)
        repo.save(customer)
        assert repo.get_by_id(1) is customer

    def test_get_by_id_missing_returns_none(self):
        repo = InMemoryCustomerRepository()
        assert repo.get_by_id(999) is None

    def test_list_all_returns_everything(self):
        repo = InMemoryCustomerRepository()
        repo.save(make_customer(1))
        repo.save(make_customer(2))
        assert sorted(c.id for c in repo.list_all()) == [1, 2]


class TestProtocolCompliance:
    """Pyright checks the structural match on these assignments."""

    def test_vehicle_repo_satisfies_protocol(self):
        repo: VehicleRepository = InMemoryVehicleRepository()
        assert repo is not None

    def test_rental_repo_satisfies_protocol(self):
        repo: RentalRepository = InMemoryRentalRepository()
        assert repo is not None

    def test_customer_repo_satisfies_protocol(self):
        repo: CustomerRepository = InMemoryCustomerRepository()
        assert repo is not None

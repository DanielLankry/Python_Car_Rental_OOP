"""Repository contracts and in-memory implementations.

Persistence boundary: this module knows about the domain, the domain knows
nothing about storage. Swapping InMemory* for a real database implementation
must not require touching entities.py.
"""

from typing import Protocol

from .entities import Customer, Rental, Vehicle
from .vehicle_status import VehicleStatus


class VehicleRepository(Protocol):
    """Contract for storing and retrieving vehicles."""

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        """Return the vehicle with this id, or None if it does not exist."""
        ...

    def save(self, vehicle: Vehicle) -> None:
        """Insert the vehicle, or overwrite the existing one with the same id."""
        ...

    def list_available(self) -> list[Vehicle]:
        """Return every vehicle whose status is AVAILABLE."""
        ...


class RentalRepository(Protocol):
    """Contract for storing and retrieving rentals."""

    def get_by_id(self, rental_id: int) -> Rental | None:
        """Return the rental with this id, or None if it does not exist."""
        ...

    def save(self, rental: Rental) -> None:
        """Insert the rental, or overwrite the existing one with the same id."""
        ...

    def list_by_customer(self, customer_id: int) -> list[Rental]:
        """Return every rental belonging to this customer."""
        ...


class CustomerRepository(Protocol):
    """Contract for storing and retrieving customers."""

    def get_by_id(self, customer_id: int) -> Customer | None:
        """Return the customer with this id, or None if it does not exist."""
        ...

    def save(self, customer: Customer) -> None:
        """Insert the customer, or overwrite the existing one with the same id."""
        ...

    def list_all(self) -> list[Customer]:
        """Return every stored customer."""
        ...


class InMemoryVehicleRepository:
    """VehicleRepository backed by a dict. Test/dev only — not persistent."""

    def __init__(self) -> None:
        self._vehicles: dict[int, Vehicle] = {}

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self._vehicles.get(vehicle_id)

    def save(self, vehicle: Vehicle) -> None:
        # Dict assignment is an upsert: inserts if the id is new,
        # overwrites if it already exists. One line covers both.
        self._vehicles[vehicle.id] = vehicle

    def list_available(self) -> list[Vehicle]:
        return [
            vehicle
            for vehicle in self._vehicles.values()
            if vehicle.status == VehicleStatus.AVAILABLE
        ]


class InMemoryRentalRepository:
    """RentalRepository backed by a dict. Test/dev only — not persistent."""

    def __init__(self) -> None:
        self._rentals: dict[int, Rental] = {}

    def get_by_id(self, rental_id: int) -> Rental | None:
        return self._rentals.get(rental_id)

    def save(self, rental: Rental) -> None:
        self._rentals[rental.id] = rental

    def list_by_customer(self, customer_id: int) -> list[Rental]:
        return [
            rental
            for rental in self._rentals.values()
            if rental.customer.id == customer_id
        ]


class InMemoryCustomerRepository:
    """CustomerRepository backed by a dict. Test/dev only — not persistent."""

    def __init__(self) -> None:
        self._customers: dict[int, Customer] = {}

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self._customers.get(customer_id)

    def save(self, customer: Customer) -> None:
        self._customers[customer.id] = customer

    def list_all(self) -> list[Customer]:
        return list(self._customers.values())

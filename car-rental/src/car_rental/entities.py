from datetime import date
from decimal import Decimal

from .pricing import PricingStrategy, StandardPricing
from .rental_status import RentalStatus
from .vehicle_status import VehicleStatus


class Vehicle:
    def __init__(
            self,
            id: int,
            manufacturer: str,
            model: str,
            year: int,
            daily_rate: Decimal,
            status:  VehicleStatus = VehicleStatus.AVAILABLE,
    ) -> None:
        
        if id < 0:
            raise ValueError("ID must be positive integer")

        if not manufacturer:
            raise ValueError("Manufacturer must be not empty string")

        if not model:
            raise ValueError("Model must be not empty string")

        if year < 1886 or year > 2025:
            raise ValueError(f"Invalid year: {year}. Must be between 1886 and 2025")

        if daily_rate < 0:
            raise ValueError("Daily rate must not be negative")

        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.status = status

    def rent(self) -> None:
        if self.status != VehicleStatus.AVAILABLE:
            raise ValueError(f"Cannot rent vehicle #{self.id}: already {self.status.value}")
        self.status = VehicleStatus.RENTED

    def return_vehicle(self) -> None:
        if self.status != VehicleStatus.RENTED:
            raise ValueError(f"Cannot return vehicle #{self.id}: status is {self.status.value}")
        self.status = VehicleStatus.AVAILABLE

    def send_to_maintenance(self) -> None:
        if self.status == VehicleStatus.MAINTENANCE:
            raise ValueError(f"Vehicle #{self.id} is already in maintenance")
        self.status = VehicleStatus.MAINTENANCE



class Customer:
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            email: str,
            license_number: str,
    ) -> None:
        
        if id <= 0:
            raise ValueError("id must be positive")
        
        if not first_name.strip():
            raise ValueError("first_name must be a non-empty string")
        
        if not last_name.strip():
            raise ValueError("last_name must be a non-empty string")
        
        if "@" not in email:
            raise ValueError("email must contain '@'")
        
        if not license_number.strip():
            raise ValueError("license_number cannot be empty")

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.license_number = license_number

class Rental:
    def __init__(
        self,
        id: int,
        customer: Customer,
        vehicle: Vehicle,
        start_date: date,
        end_date: date,
        status: RentalStatus = RentalStatus.RESERVED,
        pricing_strategy: PricingStrategy | None = None,
    ) -> None:
        
        if id <= 0:
            raise ValueError("ID must be positive")

        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        self.id = id
        self.customer = customer
        self.vehicle = vehicle
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.pricing_strategy = pricing_strategy or StandardPricing()


    def start(self) -> None:
        """Move the rental to ACTIVE and reserve the vehicle.

        Order matters: the vehicle is rented FIRST because that is the
        operation that can fail (the vehicle may not be AVAILABLE). Only
        after it succeeds do we flip the rental's own status. A failed
        start therefore leaves the rental RESERVED and the vehicle
        untouched — never a half-started rental.
        """
        if self.status != RentalStatus.RESERVED:
            raise ValueError(
                f"Cannot start rental #{self.id}: status is {self.status.value}, expected reserved"
            )
        self.vehicle.rent()  # raises if the vehicle is not AVAILABLE
        self.status = RentalStatus.ACTIVE

    def complete(self) -> None:
        """Move the rental to COMPLETED and release the vehicle.

        Same ordering rule as start(): release the vehicle FIRST (it can
        fail if the vehicle isn't currently rented), then flip the rental's
        own status. A failed complete leaves the rental ACTIVE and the
        vehicle RENTED — a consistent state.
        """
        if self.status != RentalStatus.ACTIVE:
            raise ValueError(
                f"Cannot complete rental #{self.id}: status is {self.status.value}, expected active"
            )
        self.vehicle.return_vehicle()  # raises if the vehicle is not RENTED
        self.status = RentalStatus.COMPLETED

    def cancel(self) -> None:
        # Transitions: RESERVED -> CANCELLED only (can't cancel mid-rental)
        if self.status != RentalStatus.RESERVED:
            raise ValueError(
                f"Cannot cancel rental #{self.id}: status is {self.status.value}, expected reserved"
            )
        self.status = RentalStatus.CANCELLED

    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    def total_price(self) -> Decimal:
        return self.pricing_strategy.calculate_total(self.duration_days(),self.vehicle.daily_rate)



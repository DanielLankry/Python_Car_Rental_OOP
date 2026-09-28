from decimal import Decimal

from .models import VehicleStatus


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
        
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name must be a non-empty string")
        
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name must be a non-empty string")
        
        if "@" not in email:
            raise ValueError("email must contain '@'")
        
        if not isinstance(license_number, str) or not license_number.strip():
            raise ValueError("license_number cannot be empty")

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.license_number = license_number

class Renatl:
    def __init__{
        self,
        id:int,
        customer:Customer,
        
    }
        


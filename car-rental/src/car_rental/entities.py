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



class Customer:
    def __init__(
            self,
            first_name: str,
            email:str,
            last_name:str,
            id: int,
            phone_number:int
    ) -> None:
        
        if not first_name:
            raise ValueError("Name cannot be an empty string")

        if not last_name:
            raise ValueError("Name cannot be an empty string")
        

        if not email:
            raise ValueError("email cannot be an empty string")

        if not id:
            raise ValueError("id cannot be an empty integer")

        if not phone_number:
            raise ValueError("phone number cannot be an empty integer")

        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        
        

        


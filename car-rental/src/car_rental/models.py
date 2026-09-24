from enum import Enum


class VehicleStatus(Enum):  # Each vehicle can be in one of this 3 situsations 
    AVAILABLE = "Avaliable"
    RENTED = "Rented"
    MAINTENANCE = "maintenance"

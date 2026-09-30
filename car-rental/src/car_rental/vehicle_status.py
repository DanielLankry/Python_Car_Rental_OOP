"""Vehicle status enumeration.

This module defines the possible states a vehicle can be in.
"""

from enum import Enum


class VehicleStatus(Enum):
    """Possible states a vehicle can be in.

    Using `Enum` (not plain strings) gives us:
    - Type safety at call sites (can't pass "rented" as a string).
    - An exhaustive list the type checker validates.
    - Easy JSON serialization via .value later (Phase 6).
    """
    AVAILABLE = "available"      # Vehicle can be rented right now
    RENTED = "rented"            # Currently out on a rental
    MAINTENANCE = "maintenance"  # In shop, not rentable
from dataclasses import dataclass
from typing import Tuple
from simulator.status import RiderStatus
from simulator.status import TripStage

@dataclass
class Rider:
    id: int

    location: Tuple[int, int]

    status: RiderStatus = RiderStatus.AVAILABLE

    speed: float = 0.5

    current_order = None

    target_location = None

    trip_stage: TripStage | None=None

    remaining_distance = 0

    distance_travelled: float = 0

    idle_minutes: int = 0

    busy_minutes: int = 0

    def __str__(self):
        return (
            f"Rider {self.id} | "
            f"{self.status} | "
            f"{self.location}"
        )
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Restaurant:
    id: int
    name: str
    location: Tuple[int, int]
    avg_prep_time: int

    def __str__(self):
        return (
            f"{self.name} | "
            f"Location={self.location} | "
            f"Avg Prep={self.avg_prep_time} mins"
        )
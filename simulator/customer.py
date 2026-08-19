from dataclasses import dataclass
from typing import Tuple


@dataclass
class Customer:
    id: int
    location: Tuple[int, int]

    def __str__(self):
        return (
            f"Customer {self.id} | "
            f"Location={self.location}"
        )
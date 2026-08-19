from dataclasses import dataclass

from simulator.restaurant import Restaurant
from simulator.customer import Customer
from simulator.status import OrderStatus



@dataclass
class Order:

    @property
    def preparation_time(self):
        return self.ready_time - self.order_time


    @property
    def assignment_delay(self):
        if self.assigned_time is None:
            return None
        return self.assigned_time - self.ready_time


    @property
    def pickup_delay(self):
        if self.pickup_time is None:
            return None
        return self.pickup_time - self.assigned_time


    @property
    def delivery_travel_time(self):
        if self.delivery_time is None:
            return None
        return self.delivery_time - self.pickup_time


    @property
    def total_time(self):
        if self.delivery_time is None:
            return None
        return self.delivery_time - self.order_time

    id: int

    restaurant: Restaurant

    customer: Customer

    prep_time: int

    order_time: int

    ready_time: int

    assigned_time: int | None = None
    pickup_time: int | None = None
    delivery_time: int | None = None

    assigned_rider = None

    status: OrderStatus = OrderStatus.WAITING

    def __str__(self):

        return (
            f"Order {self.id} | "
            f"{self.restaurant.name} -> Customer {self.customer.id} | "
            f"Ordered={self.order_time} | "
            f"Ready={self.ready_time} | "
            f"Status={self.status}"
        )
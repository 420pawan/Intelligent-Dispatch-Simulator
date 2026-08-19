from abc import ABC, abstractmethod

from simulator.status import RiderStatus
from simulator.status import OrderStatus
from simulator.status import TripStage
from utils.distance import euclidean


class DispatchStrategy(ABC):

    @abstractmethod
    def assign(self, city, current_time):
        pass

    def assign_order(self, rider, order, current_time):

        distance = euclidean(
            rider.location,
            order.restaurant.location
        )

        order.assigned_rider = rider
        order.status = OrderStatus.ASSIGNED
        order.assigned_time = current_time

        rider.current_order = order
        rider.status = RiderStatus.BUSY
        rider.target_location = order.restaurant.location
        rider.trip_stage = TripStage.TO_RESTAURANT
        rider.remaining_distance = distance

        return (rider, order)
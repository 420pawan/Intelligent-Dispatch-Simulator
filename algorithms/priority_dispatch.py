from utils.distance import euclidean

from simulator.status import OrderStatus
from simulator.status import RiderStatus

from algorithms.dispatch_strategy import DispatchStrategy


class PriorityDispatch(DispatchStrategy):

    def assign(self, city, current_time):

        assignments = []

        available_riders = [
            rider
            for rider in city.riders
            if rider.status == RiderStatus.AVAILABLE
        ]

        ready_orders = [
            order
            for order in city.orders
            if (
                order.status == OrderStatus.READY
                and order.assigned_rider is None
            )
        ]

        ready_orders.sort(
            key=lambda order: order.ready_time
        )

        for order in ready_orders:

            if not available_riders:
                break

            nearest_rider = min(
                available_riders,
                key=lambda rider: euclidean(
                    rider.location,
                    order.restaurant.location
                )
            )

            assignments.append(
                self.assign_order(
                    nearest_rider,
                    order,
                    current_time
                )
            )

            available_riders.remove(nearest_rider)

        return assignments
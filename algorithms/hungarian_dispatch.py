from scipy.optimize import linear_sum_assignment

from algorithms.dispatch_strategy import DispatchStrategy
from simulator.status import OrderStatus, RiderStatus
from utils.distance import euclidean


class HungarianDispatch(DispatchStrategy):

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
            if order.status == OrderStatus.READY
            and order.assigned_rider is None
        ]

        if not available_riders or not ready_orders:
            return assignments

        cost_matrix = []

        for rider in available_riders:

            row = []

            for order in ready_orders:

                row.append(
                    euclidean(
                        rider.location,
                        order.restaurant.location
                    )
                )

            cost_matrix.append(row)

        rider_indices, order_indices = linear_sum_assignment(cost_matrix)

        for r_idx, o_idx in zip(rider_indices, order_indices):

            rider = available_riders[r_idx]
            order = ready_orders[o_idx]

            assignments.append(
                self.assign_order(
                    rider,
                    order,
                    current_time
                )
            )

        return assignments
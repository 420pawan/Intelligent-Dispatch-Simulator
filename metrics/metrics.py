from simulator.status import OrderStatus
from simulator.status import RiderStatus

class Metrics:

    def __init__(self):
        self.total_orders = 0
        self.completed_orders = 0
        self.total_delivery_time = 0

    def calculate(self, city):

        snapshot = self.get_snapshot(city)

        delivered_orders = [
            order
            for order in city.orders
            if order.status == OrderStatus.DELIVERED
        ]

        prep_times = [
            order.preparation_time
            for order in delivered_orders
        ]

        avg_prep = (
            sum(prep_times) / len(prep_times)
            if prep_times else 0
        )

        wait_times = [
            order.assignment_delay
            for order in delivered_orders
        ]

        avg_wait = (
            sum(wait_times) / len(wait_times)
            if wait_times else 0
        )

        travel_times = [
            order.delivery_travel_time
            for order in delivered_orders
        ]

        avg_travel = (
            sum(travel_times) / len(travel_times)
            if travel_times else 0
        )

        pickup_times = [
            order.pickup_delay
            for order in delivered_orders
        ]

        avg_pickup = (
            sum(pickup_times) / len(pickup_times)
            if pickup_times else 0
        )

        total_times = [
            order.total_time
            for order in delivered_orders
        ]

        avg_total = (
            sum(total_times) / len(total_times)
            if total_times else 0
        )

        completion_rate = (
            snapshot["delivered"] / len(city.orders) * 100
            if city.orders else 0
        )

        total_util = 0

        for rider in city.riders:

            total = rider.idle_minutes + rider.busy_minutes

            util = (
                rider.busy_minutes / total * 100
                if total > 0 else 0
            )

            total_util += util

        avg_util = (
            total_util / len(city.riders)
            if city.riders else 0
        )

        return {
            **snapshot,
            "avg_prep": avg_prep,
            "avg_wait": avg_wait,
            "avg_travel": avg_travel,
            "avg_pickup": avg_pickup,
            "avg_total": avg_total,
            "completion_rate": completion_rate,
            "avg_util": avg_util
        }

    def print(self, city):
        metrics = self.calculate(city)

        print("\n===== RIDER UTILIZATION =====")

        total_util = 0

        for rider in city.riders:
            total = rider.idle_minutes + rider.busy_minutes

            util = 0
            if total > 0:
                util = rider.busy_minutes / total * 100

            total_util += util

            print(f"Rider {rider.id}: {util:.1f}%")

        avg_util = (
            total_util / len(city.riders)
            if city.riders else 0
        )

        print(f"\nAverage Rider Utilization : {avg_util:.1f}%")

        print("\n===== METRICS =====")

        print(f"Waiting   : {metrics['waiting']}")
        print(f"Ready     : {metrics['ready']}")
        print(f"Assigned  : {metrics['assigned']}")
        print(f"Picked Up : {metrics['picked']}")
        print(f"Delivered : {metrics['delivered']}")

        print()

        print(f"Available Riders : {metrics['available']}")
        print(f"Busy Riders      : {metrics['busy']}")

        print("\n===== DELIVERY METRICS =====")

        print(f"Average Preparation Time : {metrics['avg_prep']:.2f} min")
        print(f"Average Rider Wait Time : {metrics['avg_wait']:.2f} min")
        print(f"Average Delivery Time : {metrics['avg_travel']:.2f} min")
        print(f"Average Pickup Delay : {metrics['avg_pickup']:.2f} min")
        print(f"Average Total Time : {metrics['avg_total']:.2f} min")
        print(f"Completion Rate : {metrics['completion_rate']:.1f}%")

    def get_snapshot(self,city):
        waiting = sum(
            order.status == OrderStatus.WAITING
            for order in city.orders
        )

        ready = sum(
            order.status == OrderStatus.READY
            for order in city.orders
        )

        assigned = sum(
            order.status == OrderStatus.ASSIGNED
            for order in city.orders
        )

        picked = sum(
            order.status == OrderStatus.PICKED_UP
            for order in city.orders
        )

        delivered = sum(
            order.status == OrderStatus.DELIVERED
            for order in city.orders
        )

        available = sum(
            rider.status == RiderStatus.AVAILABLE
            for rider in city.riders
        )

        busy = len(city.riders) - available

        return {
            "waiting": waiting,
            "ready": ready,
            "assigned": assigned,
            "picked": picked,
            "delivered": delivered,
            "available": available,
            "busy": busy
        }
    



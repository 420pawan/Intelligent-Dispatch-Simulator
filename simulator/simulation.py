import random

from utils.distance import euclidean
from algorithms.nearest_dispatch import NearestDispatch
from simulator.customer import Customer
from simulator.order import Order
from metrics.metrics import Metrics
from metrics.history import MetricsHistory
from simulator.status import OrderStatus
from simulator.status import RiderStatus
from simulator.status import TripStage
from algorithms.dispatch_strategy import DispatchStrategy
from algorithms.hungarian_dispatch import HungarianDispatch

class Simulation:

    def __init__(self, city, demand_level="Normal"):

        self.city = city
        self.demand_level = demand_level

        self.current_time = 0

        self.next_order_id = 1

        self.running = True

        self.dispatcher: DispatchStrategy = HungarianDispatch()

        self.metrics = Metrics()   

        self.history = MetricsHistory(self.metrics)

    def generate_orders(self, number_of_orders):

        for _ in range(number_of_orders):

            customer = Customer(
                id=len(self.city.customers) + 1,
                location=self.city.random_location()
            )

            restaurant = random.choice(self.city.restaurants)

            prep_time = random.randint(
                restaurant.avg_prep_time - 2,
                restaurant.avg_prep_time + 2
            )

            order = Order(
                id=self.next_order_id,
                restaurant=restaurant,
                customer=customer,
                prep_time=prep_time,
                order_time=self.current_time,
                ready_time=self.current_time + prep_time
            )

            self.city.customers.append(customer)
            self.city.orders.append(order)

            self.next_order_id += 1

    def step(self):

        print(f"\n===== Minute {self.current_time} =====")

        new_orders = self.get_new_order_count()
        self.generate_orders(new_orders)

        ready_orders = self.update_order_status()

        assignments = self.dispatcher.assign(self.city, self.current_time)

        print(f"{new_orders} new orders generated")
        print(f"Ready Orders : {ready_orders}")

        for rider, order in assignments:
            print(
                f"Assigned Rider {rider.id} "
                f"-> Order {order.id}"
            )
        self.move_riders()
        self.history.record(
            self.current_time,
            self.city
        )
        self.current_time += 1

    def run(self, duration):

        while self.current_time < duration:

            self.step()
        
        self.metrics.print(self.city)
        print(self.history.time[:10])
        print(self.history.waiting[:10])
        print(self.history.busy_riders[:10])

    def update_order_status(self):

        ready = 0

        for order in self.city.orders:

            if (
                order.status == OrderStatus.WAITING
                and self.current_time >= order.ready_time
            ):
                order.status = OrderStatus.READY

            if order.status == OrderStatus.READY:
                ready += 1

        return ready
    
    def move_riders(self):

        for rider in self.city.riders:

            if rider.status == RiderStatus.AVAILABLE:
                rider.idle_minutes += 1
                continue

            rider.busy_minutes += 1

            rider.remaining_distance -= rider.speed

            rider.distance_travelled += rider.speed

            if rider.remaining_distance > 0:
                continue

            order = rider.current_order

            if rider.trip_stage == TripStage.TO_RESTAURANT:

                rider.location = order.restaurant.location

                rider.trip_stage = TripStage.TO_CUSTOMER

                rider.target_location = order.customer.location

                rider.remaining_distance = euclidean(
                    rider.location,
                    rider.target_location
                )

                order.status = OrderStatus.PICKED_UP
                order.pickup_time = self.current_time

                print(
                    f"Rider {rider.id} picked up Order {order.id}"
                )

            elif rider.trip_stage == TripStage.TO_CUSTOMER:

                rider.location = order.customer.location

                order.status = OrderStatus.DELIVERED

                order.delivery_time = self.current_time

                print(
                    f"Order {order.id} delivered by Rider {rider.id}"
                )

                rider.current_order = None
                rider.target_location = None
                rider.trip_stage = None
                rider.remaining_distance = 0
                rider.status = RiderStatus.AVAILABLE

    def get_new_order_count(self):

        if self.demand_level == "Low":
            return random.randint(0, 1)

        elif self.demand_level == "Normal":
            if random.random()<0.8:
                return 1
            else:
                return 2

        elif self.demand_level == "Peak":
            return random.randint(2, 4)

        return random.randint(1, 2)
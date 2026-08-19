import random

from simulator.restaurant import Restaurant
from simulator.rider import Rider
from simulator.customer import Customer
from simulator.order import Order


class City:

    def __init__(
        self,
        width=8,
        height=8,
        restaurants=10,
        riders=20
    ):

        self.width = width
        self.height = height

        self.restaurants = []
        self.riders = []

        self.customers = []
        self.orders = []

        self.generate_restaurants(restaurants)
        self.generate_riders(riders)

    def random_location(self):
        return (
            random.randint(0, self.width),
            random.randint(0, self.height)
        )

    def generate_restaurants(self, n):

        for i in range(n):

            self.restaurants.append(
                Restaurant(
                    id=i + 1,
                    name=f"Restaurant_{i+1}",
                    location=self.random_location(),
                    avg_prep_time=random.randint(8, 18)
                )
            )

    def generate_riders(self, n):

        for i in range(n):

            self.riders.append(
                Rider(
                    id=i + 1,
                    location=self.random_location()
                )
            )

    # def generate_orders(self, n):

    #     self.orders.clear()
    #     self.customers.clear()

    #     for i in range(n):

    #         customer = Customer(
    #             id=i + 1,
    #             location=self.random_location()
    #         )

    #         restaurant = random.choice(self.restaurants)

    #         order = Order(
    #             id=i + 1,
    #             restaurant=restaurant,
    #             customer=customer,
    #             prep_time=random.randint(restaurant.avg_prep_time - 2,
    #                                      restaurant.avg_prep_time + 2)
    #         )

    #         self.customers.append(customer)
    #         self.orders.append(order)

    def print_state(self):

        print("\n=========== RESTAURANTS ===========")

        for restaurant in self.restaurants:
            print(restaurant)

        print("\n============= RIDERS =============")

        for rider in self.riders:
            print(rider)

        print("\n============= ORDERS =============")

        for order in self.orders:
            print(order)
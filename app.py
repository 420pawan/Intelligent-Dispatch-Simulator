from simulator.city import City
from simulator.simulation import Simulation


def main():

    city = City(
        restaurants=8,
        riders=15
    )

    simulation = Simulation(city)

    simulation.run(duration=30)

    print("\n========== FINAL ORDERS ==========")

    for order in city.orders:

        print(order)


if __name__ == "__main__":
    main()
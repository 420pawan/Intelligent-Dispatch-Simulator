import random
import statistics

from simulator.city import City
from simulator.simulation import Simulation

from algorithms.nearest_dispatch import NearestDispatch
from algorithms.priority_dispatch import PriorityDispatch
from algorithms.hungarian_dispatch import HungarianDispatch

from experiments.experiment_result import ExperimentResult

class ExperimentRunner:

    def __init__(self):

        self.strategies = {
            "Nearest": NearestDispatch,
            "Priority": PriorityDispatch,
            "Hungarian": HungarianDispatch
        }
    
    def _run_single(self,strategy_class,duration,restaurants,riders,seed, demand_level):
        random.seed(seed)

        city = City(
            restaurants=restaurants,
            riders=riders
        )

        simulation = Simulation(city, demand_level=demand_level)

        simulation.dispatcher = strategy_class()

        simulation.run(duration)

        metrics = simulation.metrics.calculate(city)

        return ExperimentResult(
            strategy_name=strategy_class.__name__,
            metrics=metrics
        )
    
    def run(self,duration,restaurants,riders,seeds=range(1,11), demand_level="Normal"):

        all_results = {
            name:[]
            for name in self.strategies
        }

        for seed in seeds:

            for name, strategy_class in self.strategies.items():

                result = self._run_single(
                    strategy_class=strategy_class,
                    duration=duration,
                    restaurants=restaurants,
                    riders=riders,
                    seed=seed,
                    demand_level=demand_level
                )

                all_results[name].append(result.metrics)

        results = []
        for name,strategy_class in self.strategies.items():
            aggregated_metrics= self._aggregate(
                all_results[name]
            )

            results.append(
                ExperimentResult(
                    strategy_name=strategy_class.__name__,
                    metrics=aggregated_metrics
                )
            )
        return results
    
    def _aggregate(self,runs):
        metrics_to_average = [
            "completion_rate",
            "avg_total",
            "avg_pickup",
            "avg_util",
            "avg_prep",
            "avg_wait",
            "avg_travel"
        ]

        aggregated = {}

        for metric in metrics_to_average:

            values = [
                run[metric]
                for run in runs
            ]

            aggregated[metric] = statistics.mean(values)

            aggregated[f"{metric}_std"] = (
                statistics.stdev(values)
                if len(values) > 1
                else 0
            )

        return aggregated
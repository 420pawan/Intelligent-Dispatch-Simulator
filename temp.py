from experiments.experiments_runner import ExperimentRunner
from experiments.recommendation import Recommendation

runner = ExperimentRunner()

results = runner.run(
    duration=30,
    restaurants=10,
    riders=20,
    seed=42
)
recommendation = Recommendation()
result = recommendation.generate(results)
print(result)

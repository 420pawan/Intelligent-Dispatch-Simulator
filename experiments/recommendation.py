class Recommendation:

    def generate(self, results):

        best = max(
            results,
            key=lambda result: result.metrics["completion_rate"]
        )

        return {
            "best_strategy": best.strategy_name,
            "reason": "Highest completion rate"
        }
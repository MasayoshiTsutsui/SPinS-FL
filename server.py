import flwr as fl
from typing import List, Tuple, Optional
from constants import GROUP_NUM

class AggregateCustomMetricStrategy(fl.server.strategy.FedAvg):
	def aggregate_evaluate(
		self,
		rnd: int,
		results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.typing.EvaluateRes]],
		failures: List[BaseException],
		) -> Optional[float]:
		"""Aggregate evaluation losses using weighted average."""
		if not results:
			return None

		# Weigh accuracy of each client by number of examples used
		accuracies = [r.metrics["accuracy"] * r.num_examples for _, r in results]
		examples = [r.num_examples for _, r in results]

		# Aggregate and print custom metric
		accuracy_aggregated = sum(accuracies) / sum(examples)
		print(accuracy_aggregated)

		# Call aggregate_evaluate from base class (FedAvg)
		return super().aggregate_evaluate(rnd, results, failures)

# Create strategy and run server
strategy = AggregateCustomMetricStrategy(
	min_fit_clients=GROUP_NUM,
	min_evaluate_clients=GROUP_NUM,
	min_available_clients=GROUP_NUM,
)

fl.server.start_server(
					server_address="0.0.0.0:8080",
		       		config=fl.server.ServerConfig(num_rounds=150),
					strategy=strategy)

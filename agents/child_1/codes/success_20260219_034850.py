from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Dict, Union, Tuple
import threading
import json

class EnhancedOperationManager:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.operations = {}
        self.metrics_lock = threading.Lock()

    def register_operation(self, name: str, func: Callable[[Union[int, float]], Union[int, float]], description: str = ""):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' already exists: {self.operations[name].description}")
        self.operations[name] = Operation(name, func, description)

    def unregister_operation(self, name: str):
        if name in self.operations:
            del self.operations[name]
        else:
            raise ValueError(f"Operation '{name}' does not exist.")

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        valid_data, invalid_data = self.validate_data(data)

        if invalid_data:
            results["errors"].extend(invalid_data)

        if not valid_data:
            results["errors"].append("No valid data to process.")
            return results

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}

            for future in as_completed(future_to_data):
                item_results = future.result()
                results['results'].extend(item_results['results'])
                results['errors'].extend(item_results['errors'])

        self._aggregate_metrics()
        self._log_metrics(results)

        return results

    def validate_data(self, data: List[Union[int, float]]) -> Tuple[List[Union[int, float]], List[str]]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [
            f"{item} is not a valid number." for item in data if not isinstance(item, (int, float))
        ]
        return valid_data, invalid_data

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        for op_name in chosen_operations:
            operation = self.operations.get(op_name)
            if not operation:
                results['errors'].append(f"[ERROR] Operation '{op_name}' is not registered.")
                continue

            try:
                result = operation.execute(item)
                results['results'].append(result)
                operation.success_count += 1
            except Exception as e:
                results['errors'].append(f"[ERROR] {f'Operation failed: {e}'}")
                operation.error_count += 1
                
        return results

    def _aggregate_metrics(self):
        with self.metrics_lock:
            metrics_data = {name: {"successes": op.success_count, "errors": op.error_count} for name, op in self.operations.items()}
            print("\nAggregated summary of operations:", json.dumps(metrics_data, indent=2))

    def _log_metrics(self, results: dict):
        with self.metrics_lock:
            with open('metrics_log.json', 'a') as log_file:
                log_file.write(json.dumps(results) + "\n")
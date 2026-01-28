import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Union

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name
        self.success_count = 0
        self.error_count = 0

    def apply(self, value: Union[int, float]) -> Union[str, float]:
        try:
            result = self.func(value)
            self.success_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            return self._format_error_message(e)

    def _format_error_message(self, error: Exception) -> str:
        return f"Error in '{self.name}': {str(error)}"

class OperationManager:
    def __init__(self, max_workers: int = 5):
        self.operations: Dict[str, Operation] = {}
        self.max_workers = max_workers

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def remove_operation(self, name: str):
        if name in self.operations:
            del self.operations[name]

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        
        if not data:
            results["errors"].append("No valid data to process.")
            return results

        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                operation_results = future.result()
                results["results"].extend([result for result in operation_results if isinstance(result, (int, float))])
                results["errors"].extend([result for result in operation_results if isinstance(result, str)])

        if invalid_data:
            results["errors"].append(f"Invalid data encountered: {invalid_data}")

        self._log_metrics()
        self._save_log_to_file()
        return results

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        for name in chosen_operations:
            if name not in self.operations:
                results.append(f"Error: Operation '{name}' is not registered.")
            else:
                result = self.operations[name].apply(item)
                results.append(result)
        return results

    def _log_metrics(self):
        print("\nSummary of operations:")
        for op in self.operations.values():
            print(f"{op.name}: Successes: {op.success_count}, Errors: {op.error_count}")

    def _save_log_to_file(self, filename="operation_metrics.json"):
        metrics_data = {op.name: {"successes": op.success_count, "errors": op.error_count} for op in self.operations.values()}
        with open(filename, "w") as f:
            json.dump(metrics_data, f)
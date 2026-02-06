import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Union

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name
        self.success_count = 0
        self.error_count = 0
    
    def apply(self, value):
        try:
            result = self.func(value)
            self.success_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            return f"[ERROR-{self.name}] {str(e)}"

class OperationManager:
    def __init__(self, max_workers: int = 5):
        self.operations: Dict[str, Operation] = {}
        self.max_workers = max_workers

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            return f"[ERROR] Operation '{name}' is already registered."
        self.operations[name] = Operation(func, name)
        return f"[INFO] Operation '{name}' registered."

    def remove_operation(self, name: str):
        if name not in self.operations:
            return f"[ERROR] Operation '{name}' not found."
        del self.operations[name]
        return f"[INFO] Operation '{name}' removed."

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        valid_data = [item for item in data if isinstance(item, (int, float))]

        if not valid_data:
            results["errors"].append("No valid data to process.")
            return results

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                item_results = future.result()
                results["results"].extend(item_results.get('results', []))
                results["errors"].extend(item_results.get('errors', []))

        results['errors'].extend([item for item in data if not isinstance(item, (int, float))])
        self._log_metrics()
        self._save_log_to_file()
        return results

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        for name in chosen_operations:
            if name not in self.operations:
                results['errors'].append(f"[ERROR] Operation '{name}' is not registered.")
                continue
            result = self.operations[name].apply(item)
            # 新しいエラーハンドリング
            if isinstance(result, str) and result.startswith("[ERROR]"):
                results['errors'].append(result)
            else:
                results['results'].append(result)
        return results

    def _log_metrics(self):
        metrics_data = {op.name: {"successes": op.success_count, "errors": op.error_count} for op in self.operations.values()}
        print("\nSummary of operations:", json.dumps(metrics_data, indent=2))

    def _save_log_to_file(self, filename="operation_metrics.json"):
        metrics_data = {op.name: {"successes": op.success_count, "errors": op.error_count} for op in self.operations.values()}
        with open(filename, "w") as f:
            json.dump(metrics_data, f)

    def validate_data(self, data: List[Union[int, float]]) -> bool:
        return all(isinstance(item, (int, float)) for item in data)
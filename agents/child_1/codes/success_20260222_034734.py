import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Callable, Union, Dict
import threading

class OperationManager:
    def __init__(self, max_workers=4):
        self.operations: Dict[str, Callable[[Union[int, float]], Union[int, float]]] = {}
        self.metrics_lock = threading.Lock()
        self.max_workers = max_workers

    def register_operation(self, name: str, func: Callable[[Union[int, float]], Union[int, float]], description: str = ""):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' already exists: {description}")
        self.operations[name] = func

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
                self._log_metrics(item_results)  # ログの改善

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
            if operation is None:
                results['errors'].append(f"[ERROR] Operation '{op_name}' is not registered.")
                continue

            retry_count = 3
            for attempt in range(retry_count):
                try:
                    result = operation(item)
                    results['results'].append(result)
                    break  # 成功したらループを抜ける
                except Exception as e:
                    results['errors'].append(f"[ERROR] Attempt {attempt + 1} failed for operation '{op_name}': {e}")
                    if attempt == retry_count - 1:
                        results['errors'].append(f"[ERROR] Final attempt failed for operation '{op_name}'.")

        return results

    def _aggregate_metrics(self):
        # メトリクス集計ロジックをここに実装する
        pass

    def _log_metrics(self, results: dict):
        with self.metrics_lock:
            with open('metrics_log.json', 'a') as log_file:
                log_file.write(json.dumps({
                    "results": results['results'],
                    "errors": results['errors'],
                    "timestamp": datetime.now().isoformat()
                }) + "\n")
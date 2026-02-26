import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Tuple, Callable

class OperationManager:
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.operations: dict[str, Callable] = {}
        self.metrics_lock = threading.Lock()
        self.retry_attempts = 3

    def register_operation(self, name: str, operation: Callable):
        self.operations[name] = operation

    def unregister_operation(self, name: str):
        if name in self.operations:
            del self.operations[name]
        else:
            logging.error(f"Operation '{name}' does not exist.")

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        valid_data, invalid_data = self.validate_data(data)
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

        self._aggregate_metrics(results)
        return results

    def validate_data(self, data: List[Union[int, float]]) -> Tuple[List[Union[int, float]], List[str]]:
        valid_data = []
        invalid_data = []
        for item in data:
            if not isinstance(item, (int, float)):
                invalid_data.append(f"Error: {item} is not a valid number.")
            else:
                valid_data.append(item)
        return valid_data, invalid_data

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        for op_name in chosen_operations:
            operation = self.operations.get(op_name)
            if operation is None:
                results['errors'].append(f"Error: Operation '{op_name}' is not registered.")
                continue

            results = self._execute_with_retry(operation, item, results, op_name)
        
        return results

    def _execute_with_retry(self, operation: Callable, item: Union[int, float], results: dict, op_name: str) -> dict:
        for attempt in range(self.retry_attempts):
            try:
                result = operation(item)
                results['results'].append(result)
                break 
            except Exception as e:
                logging.error(f"Operation '{op_name}' failed: {e} (Attempt {attempt + 1})")
                if attempt == self.retry_attempts - 1:
                    results['errors'].append(f"Error: Operation '{op_name}' failed after {self.retry_attempts} attempts.")
        return results

    def _aggregate_metrics(self, results: dict):
        # メトリクスを集計し、より詳細な情報を提供する処理を実装
        self._log_metrics(results)

    def _log_metrics(self, results: dict):
        with self.metrics_lock:
            with open('metrics_log.json', 'a') as log_file:
                log_file.write(json.dumps({
                    "results": results['results'],
                    "errors": results['errors'],
                    "timestamp": datetime.now().isoformat()
                }) + "\n")
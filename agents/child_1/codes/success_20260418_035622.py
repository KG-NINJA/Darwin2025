import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Tuple

class EnhancedOperationManager:
    def __init__(self):
        self.operations: Dict[str, Tuple[Callable[[Any], Any], Dict[str, Any]]] = {}
        self.errors = []
        self.successes = []
    
    def register_operation(self, name: str, operation: Callable[[Any], Any], options: Dict[str, Any] = None) -> None:
        self.operations[name] = (operation, options or {})

    def dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = None) -> Dict[str, Any]:
        results = {'successes': [], 'errors': []}
        max_workers = self._initialize_worker_count(max_workers, data)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_with_options, item, op_name): item 
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                self._handle_future_result(future, item, results)

        return results

    def _initialize_worker_count(self, max_workers: int, data: List[Any]) -> int:
        return min(max_workers or len(data), 10)

    def _execute_with_options(self, item: Any, operation_name: str) -> Tuple[bool, Any, str]:
        operation, options = self.operations[operation_name]
        retries = options.get('retries', 1)
        max_delay = options.get('max_delay', 3)

        for attempt in range(retries):
            delay = min(max_delay, (attempt + 1) ** 2)
            success, result, error_msg = self._run_single_operation(item, operation)

            if success:
                return (True, item, result)
            logging.error(f"Retrying {operation_name} for item {item}: {error_msg} (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)

        return (False, item, f"Operation '{operation_name}' failed after {retries} attempts: {error_msg}")

    def _run_single_operation(self, item: Any, operation: Callable[[Any], Any]) -> Tuple[bool, Any, str]:
        try:
            result = operation(item)
            return (True, result, None)
        except Exception as e:
            return (False, None, f"Operation '{operation.__name__}' for item '{item}' failed due to: {str(e)}")

    def _handle_future_result(self, future, item: Any, results: Dict[str, Any]):
        try:
            success, item, result = future.result()
            if success:
                results['successes'].append((item, result))
            else:
                results['errors'].append((item, result))
        except Exception as e:
            results['errors'].append((item, f"Unexpected Error while processing item '{item}': {str(e)}"))
from typing import List, Dict, Any, Callable, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

class Result:
    def __init__(self):
        self.successes: List[Tuple[Any, Any]] = []
        self.errors: List[Tuple[Any, str]] = []

    def add_success(self, item: Any, result: Any) -> None:
        self.successes.append((item, result))

    def add_error(self, item: Any, error_msg: str) -> None:
        self.errors.append((item, error_msg))

    def to_dict(self) -> Dict[str, List[Tuple]]:
        return {
            'successes': self.successes,
            'errors': self.errors
        }

class EnhancedOperationManager:
    def __init__(self):
        self.operations: Dict[str, Tuple[Callable[[Any], Any], int]] = {}
        
    def register_operation(self, name: str, operation: Callable[[Any], Any], retries: int = 3) -> None:
        self.operations[name] = (operation, retries)

    def run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = None) -> Dict[str, Any]:
        results = Result()
        max_workers = self._initialize_worker_count(max_workers, data)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_with_retries, item, op_name): item 
                       for item in data 
                       for op_name in chosen_operations
                       if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                self._handle_future_result(future, item, results)

        return results.to_dict()

    def _initialize_worker_count(self, max_workers: int, data: List[Any]) -> int:
        return max_workers or (len(data) if len(data) > 1 else 1)

    def _execute_with_retries(self, item: Any, operation_name: str) -> Tuple[bool, Any, str]:
        operation, retries = self.operations[operation_name]
        for attempt in range(retries):
            success, result, error_msg = self._run_single_operation(item, operation)
            if success:
                return (True, item, result)
            error_msg = f"{error_msg} (Attempt {attempt + 1}/{retries})"
        return (False, item, error_msg)

    def _run_single_operation(self, item: Any, operation: Callable[[Any], Any]) -> Tuple[bool, Any, str]:
        try:
            result = operation(item)
            return (True, result, None)
        except Exception as e:
            return (False, None, f"Operation '{operation.__name__}' failed for item '{item}': {str(e)}")

    def _handle_future_result(self, future, item: Any, results: Result):
        try:
            success, item, result = future.result()
            if success:
                results.add_success(item, result)
            else:
                results.add_error(item, result)
        except Exception as e:
            results.add_error(item, f"Unexpected error: {str(e)}")

# 例示的な使用
if __name__ == "__main__":
    manager = EnhancedOperationManager()
    manager.register_operation("double", lambda x: x * 2 if isinstance(x, (int, float)) else (1/0), retries=2)
    manager.register_operation("uppercase", lambda x: x.upper() if isinstance(x, str) else (1/0), retries=3)
    result = manager.run_operations(["hello", 1, 2, 3, None], ["double", "uppercase", "undefined_operation"], max_workers=3)
    print(result)
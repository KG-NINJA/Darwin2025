from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Dict, Union, Any

class OperationResult:
    def __init__(self, success=None, error=None):
        self.success = success
        self.error = error

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name

    def apply(self, item: Union[int, float]) -> float:
        return self.func(item)

class OperationManager:
    def __init__(self):
        self.operations: Dict[str, Operation] = {}

    def register_operation(self, func: Callable[[float], float], name: str = "Unknown"):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Union[int, float]]) -> List[OperationResult]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]
        results = []

        max_workers = min(5, len(valid_data)) if valid_data else 1
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(op.apply, item): (item, op.name)
                       for op in self.operations.values() for item in valid_data}

            for future in as_completed(futures):
                item, operation_name = futures[future]
                results.append(self.handle_future_result(future, operation_name, item))

        self.visualize_results(results, invalid_data)
        return results

    def handle_future_result(self, future, operation_name: str, item: Any) -> OperationResult:
        try:
            result = future.result()
            return OperationResult(success=result)
        except Exception as e:
            return OperationResult(error=self.format_error_message(operation_name, item, e))

    def format_error_message(self, operation_name: str, item: Any, exception: Exception) -> str:
        return f"Operation '{operation_name}' failed with: {str(exception)} (Data: {item})"

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        summary = []
        with open('results_log.txt', 'a') as log_file:
            for result in results:
                summary_line = f"Success: {result.success}" if result.success is not None else f"Error: {result.error}"
                log_file.write(f"{summary_line}\n")
                summary.append(summary_line)

            if invalid_data:
                log_file.write("Skipped invalid data:\n" + "\n".join(f"Invalid data: {item}" for item in invalid_data))

        print("\n".join(summary))

# Usage example
operation_manager = OperationManager()
operation_manager.register_operation(lambda x: x + 1, "Increment")
operation_manager.register_operation(lambda x: x ** 3, "Cube")
operation_manager.register_operation(lambda x: x ** 2, "Square")

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data)
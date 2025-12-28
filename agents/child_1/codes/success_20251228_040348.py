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

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str] = None) -> List[OperationResult]:
        chosen_operations = chosen_operations or self.operations.keys()
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]
        results = []

        max_workers = min(5, len(valid_data)) if valid_data else 1
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.operations[name].apply, item): (item, name)
                       for name in chosen_operations if name in self.operations for item in valid_data}

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
def create_operations(manager: OperationManager):
    operations = {
        "Increment": lambda x: x + 1,
        "Cube": lambda x: x ** 3,
        "Square": lambda x: x ** 2
    }
    for name, func in operations.items():
        manager.register_operation(func, name)

operation_manager = OperationManager()
create_operations(operation_manager)

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data, chosen_operations=["Increment", "Cube"])
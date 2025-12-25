from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Callable, Dict, Any

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
        results = []
        valid_data, invalid_data = self.validate_data(data)

        with ThreadPoolExecutor(max_workers=min(5, len(valid_data))) as executor:
            futures = {executor.submit(op.apply, item): (item, op.name)
                       for op in self.operations.values() for item in valid_data}

            for future in as_completed(futures):
                item, operation_name = futures[future]
                results.append(self.handle_future_result(future, operation_name, item))

        self.visualize_results(results, invalid_data)
        return results

    def validate_data(self, data: List[Any]) -> (List[float], List[Any]):
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]
        return valid_data, invalid_data

    def handle_future_result(self, future, operation_name: str, item: Any) -> OperationResult:
        try:
            result = future.result()
            return OperationResult(success=result)
        except Exception as e:
            error_message = f"Operation '{operation_name}' failed with: {str(e)} (Data: {item})"
            return OperationResult(error=error_message)

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        summary = []
        with open('results_log.txt', 'a') as log_file:
            for result in results:
                if result.success is not None:
                    summary_line = f"Success: {result.success}"
                    log_file.write(f"{summary_line}\n")
                    summary.append(summary_line)
                if result.error:
                    summary_line = f"Error: {result.error}"
                    log_file.write(f"{summary_line}\n")
                    summary.append(summary_line)

            if invalid_data:
                log_file.write("Skipped invalid data:\n")
                for item in invalid_data:
                    log_file.write(f"Invalid data: {item}\n")
                    summary.append(f"Invalid data: {item}")

        # Improved rendering
        print("\n".join(summary))

# Usage example
operation_manager = OperationManager()
operation_manager.register_operation(lambda x: x + 1, "Increment")
operation_manager.register_operation(lambda x: x ** 3, "Cube")
operation_manager.register_operation(lambda x: x ** 2, "Square")

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data)
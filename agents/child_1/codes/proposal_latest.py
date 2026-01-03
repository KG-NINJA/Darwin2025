from typing import List, Union, Callable, Any
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class OperationResult:
    def __init__(self, success: Any = None, error: str = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self):
        self.operations = {}
        self.lock = Lock()

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> List[OperationResult]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]
        results = []

        if not valid_data:
            results.append(OperationResult(error="No valid data to process."))
            results.extend(self.log_invalid_data(invalid_data))
            return results

        max_workers = min(5, len(valid_data))
        
        def worker(item: Union[int, float]):
            errors = []
            for name in chosen_operations:
                if name not in self.operations:
                    errors.append(f"Error: Operation '{name}' is not registered.")
                    continue

                try:
                    result = self.operations[name].apply(item)
                    with self.lock:
                        results.append(OperationResult(success=result))
                except ZeroDivisionError:
                    errors.append(f"Operation '{name}' failed with: division by zero.")
                except Exception as e:
                    errors.append(f"Operation '{name}' failed with: {str(e)}")

            if errors:
                with self.lock:
                    for error in errors:
                        results.append(OperationResult(error=error))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(worker, valid_data)

        self.visualize_results(results, invalid_data)
        return results

    def log_invalid_data(self, invalid_data: List[Any]) -> List[OperationResult]:
        return [OperationResult(error=f"Skipped invalid data: {item}") for item in invalid_data]

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        with open('results_log.txt', 'a') as log_file:
            for result in results:
                if result.success is not None:
                    log_file.write(f"Success: {result.success}\n")
                elif result.error:
                    log_file.write(f"Error: {result.error}\n")

            if invalid_data:
                log_file.write("Skipped invalid data:\n" + '\n'.join(f"Invalid data: {item}" for item in invalid_data))

def create_operations(manager: OperationManager):
    operations = {
        "Increment": lambda x: x + 1,
        "Cube": lambda x: x ** 3,
        "Square": lambda x: x ** 2,
        "Safe Divide": lambda x: 10 / x if x != 0 else float('inf')
    }
    for name, func in operations.items():
        manager.register_operation(func, name)

operation_manager = OperationManager()
create_operations(operation_manager)

data = [1, 2, 0, 'invalid', 4, 5]
results = operation_manager.run_operations(data, chosen_operations=["Increment", "Cube", "Safe Divide"])
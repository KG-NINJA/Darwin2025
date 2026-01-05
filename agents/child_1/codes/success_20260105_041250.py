from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Union

class OperationResult:
    def __init__(self, success=None, error=None):
        self.success = success
        self.error = error

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name

    def apply(self, value: float) -> float:
        return self.func(value)

class OperationManager:
    def __init__(self):
        self.operations = {}
        self.lock = None
        self.cache = {}

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> List[OperationResult]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        results = []

        if not valid_data:
            results.append(OperationResult(error="No valid data to process."))
            return results

        with ThreadPoolExecutor() as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                results.extend(future.result())

        self.visualize_results(results)
        return results

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> List[OperationResult]:
        results = []
        errors = []
        for name in chosen_operations:
            if name not in self.operations:
                errors.append(f"Error: Operation '{name}' is not registered.")
                continue

            try:
                result = self.operations[name].apply(item)
                results.append(OperationResult(success=result))
            except ZeroDivisionError:
                errors.append(f"Operation '{name}' failed with: division by zero.")
            except Exception as e:
                errors.append(f"Operation '{name}' failed with: {str(e)}")

        if errors:
            results.extend(OperationResult(error=error) for error in errors)
        return results

    def visualize_results(self, results: List[OperationResult]):
        with open('results_log.txt', 'a') as log_file:
            successes = [r.success for r in results if r.success is not None]
            errors = [r.error for r in results if r.error]

            log_file.write("Successes:\n" + '\n'.join(str(s) for s in successes if s) + '\n')
            log_file.write("Errors:\n" + '\n'.join(str(e) for e in errors) + '\n')

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
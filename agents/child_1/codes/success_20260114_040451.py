from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Optional, Union

class Operation:
    def __init__(self, func: Callable[[float], float], name: str, reliable: bool = True):
        self.func = func
        self.name = name
        self.reliable = reliable
        self.success_count = 0
        self.error_count = 0

    def apply(self, value: float) -> Optional[float]:
        try:
            if not self.reliable and value <= 0:
                self.error_count += 1
                return f"Error: Unsafe value for '{self.name}'."
            result = self.func(value)
            self.success_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            return f"Error in '{self.name}': {str(e)}"

class OperationManager:
    def __init__(self):
        self.operations = {}

    def register_operation(self, func: Callable[[float], float], name: str, reliable: bool = True):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name, reliable)

    def remove_operation(self, name: str):
        if name in self.operations:
            del self.operations[name]

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        errors = []
        valid_data = [item for item in data if isinstance(item, (int, float))]

        if not valid_data:
            return ["No valid data to process."]

        max_workers = min(4, len(valid_data))  # Adjust worker size based on data
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                operation_results = future.result()
                results.extend([result for result in operation_results if isinstance(result, (int, float))])
                errors.extend([result for result in operation_results if isinstance(result, str)])
                
                # Improved visual feedback
                print(f"Processed: {future_to_data[future]} => Results: {operation_results}\n")

        # Feedback on success and errors
        print("\nSummary of operations:")
        for op in self.operations.values():
            print(f"{op.name}: Successes: {op.success_count}, Errors: {op.error_count}")

        return results, errors

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        for name in chosen_operations:
            if name not in self.operations:
                results.append(f"Error: Operation '{name}' is not registered.")
            else:
                result = self.operations[name].apply(item)
                results.append(result)
        return results

def create_operations(manager: OperationManager):
    operations = {
        "Increment": lambda x: x + 1,
        "Cube": lambda x: x ** 3,
        "Square": lambda x: x ** 2,
        "Safe Divide": lambda x: 10 / x if x != 0 else float("inf")  # Handle division by zero
    }
    for name, func in operations.items():
        manager.register_operation(func, name)
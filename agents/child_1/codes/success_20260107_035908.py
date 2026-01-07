from typing import Callable, List, Union, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name

    def apply(self, value: float) -> Optional[float]:
        try:
            return self.func(value)
        except ZeroDivisionError:
            return float('inf')

class OperationManager:
    def __init__(self):
        self.operations = {}

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def remove_operation(self, name: str):
        if name in self.operations:
            del self.operations[name]

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        valid_data = [item for item in data if isinstance(item, (int, float))]

        if not valid_data:
            return ["No valid data to process."]

        with ThreadPoolExecutor() as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                results.extend(future.result())

        self.visualize_results(results)
        return results

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        for name in chosen_operations:
            if name not in self.operations:
                results.append(f"Error: Operation '{name}' is not registered.")
                continue
            result = self.operations[name].apply(item)
            if result == float('inf'):
                results.append(f"Operation '{name}' failed with: division by zero for input {item}.")
            else:
                results.append(result)

        return results

    def visualize_results(self, results: List[Union[str, float]]):
        with open('results_log.txt', 'a') as log_file:
            successes = [r for r in results if isinstance(r, (int, float))]
            errors = [r for r in results if isinstance(r, str)]

            log_file.write("Successes:\n" + '\n'.join(str(s) for s in successes) + '\n')
            log_file.write("Errors:\n" + '\n'.join(str(e) for e in errors) + '\n')

def create_operations(manager: OperationManager):
    operations = {
        "Increment": lambda x: x + 1,
        "Cube": lambda x: x ** 3,
        "Square": lambda x: x ** 2,
        "Safe Divide": lambda x: 10 / x
    }
    for name, func in operations.items():
        manager.register_operation(func, name)

# ここからコード実行
operation_manager = OperationManager()
create_operations(operation_manager)

data = [1, 2, 0, 'invalid', 4, 5]
results = operation_manager.run_operations(data, chosen_operations=["Increment", "Cube", "Safe Divide"])
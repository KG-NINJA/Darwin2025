import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Union

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name
        self.success_count = 0
        self.error_count = 0

    def apply(self, value: float) -> Union[str, float]:
        try:
            result = self.func(value)
            self.success_count += 1
            return result
        except Exception as e:
            self.error_count += 1
            return f"Error in '{self.name}': {str(e)}"

class OperationManager:
    def __init__(self):
        self.operations = {}

    def register_operation(self, func: Callable[[float], float], name: str):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def remove_operation(self, name: str):
        if name not in self.operations:
            raise ValueError(f"Operation '{name}' is not registered.")
        del self.operations[name]

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = []
        errors = []
        valid_data = [item for item in data if isinstance(item, (int, float))]

        if not valid_data:
            return {"results": results, "errors": ["No valid data to process."]}

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                operation_results = future.result()
                results.extend([result for result in operation_results if isinstance(result, (int, float))])
                errors.extend([result for result in operation_results if isinstance(result, str)])

        self._log_metrics()
        self._save_log_to_file()  # 新しいメソッドを呼び出し
        return {"results": results, "errors": errors}

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> List[Union[str, float]]:
        results = []
        for name in chosen_operations:
            if name not in self.operations:
                results.append(f"Error: Operation '{name}' is not registered.")
            else:
                result = self.operations[name].apply(item)
                results.append(result)
        return results

    def _log_metrics(self):
        print("\nSummary of operations:")
        for op in self.operations.values():
            print(f"{op.name}: Successes: {op.success_count}, Errors: {op.error_count}")

    def _save_log_to_file(self):
        metrics_data = {op.name: {"successes": op.success_count, "errors": op.error_count} for op in self.operations.values()}
        with open("operation_metrics.json", "w") as f:
            json.dump(metrics_data, f)

# 使用例
def create_operations(manager: OperationManager):
    operations = {
        "Increment": lambda x: x + 1,
        "Cube": lambda x: x ** 3,
        "Square": lambda x: x ** 2,
        "Safe Divide": lambda x: 10 / x if x != 0 else float("inf"),
        "Double": lambda x: x * 2
    }
    for name, func in operations.items():
        manager.register_operation(func, name)
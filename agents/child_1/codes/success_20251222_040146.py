from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any, Dict, Optional, Union

class Operation:
    def __init__(self, func: Callable[[float], float], name: str = "Unknown"):
        self.func = func
        self.name = name

    def apply(self, item: float) -> float:
        return self.func(item)

class OperationResult:
    def __init__(self, success: Optional[float] = None, error: Optional[str] = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self):
        self.operations: Dict[str, Operation] = {}

    def register_operation(self, func: Callable[[float], float], name: str = "Unknown"):
        if name in self.operations:
            raise ValueError(f"Operation '{name}' is already registered.")
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Union[int, float]]) -> List[OperationResult]:
        results = []
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [item for item in data if not isinstance(item, (int, float))]

        max_workers = min(5, max(1, len(valid_data) // 10))
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
            error_message = f"操作 '{operation_name}' でエラー: {str(e)} (データ: {item})"
            return OperationResult(error=error_message)

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        with open('results_log.txt', 'a') as log_file:
            for result in results:
                if result.success is not None:
                    log_file.write(f"成功: {result.success}\n")
                    print(f"成功: {result.success}")
                if result.error:
                    log_file.write(f"エラー: {result.error}\n")
                    print(f"エラー: {result.error}")

            if invalid_data:
                log_file.write("スキップされた無効なデータ:\n")
                for item in invalid_data:
                    log_file.write(f"無効なデータ: {item}\n")
                    print(f"無効なデータ: {item}")

# 使用例
operation_manager = OperationManager()
operation_manager.register_operation(lambda x: x + 1, "Increment")
operation_manager.register_operation(lambda x: x ** 3, "Cube")
operation_manager.register_operation(lambda x: x ** 2, "Square")

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data)
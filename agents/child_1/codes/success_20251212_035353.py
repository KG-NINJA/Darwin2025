from typing import List, Any, Dict, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class Operation:
    def apply(self, item: float) -> float:
        raise NotImplementedError("This method should be overridden in subclasses.")

class Increment(Operation):
    def apply(self, item: float) -> float:
        return item + 1

class Cube(Operation):
    def apply(self, item: float) -> float:
        return item ** 3

class OperationResult:
    def __init__(self, success: Optional[float] = None, error: Optional[str] = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}

    def register_operation(self, name: str, operation: Operation):
        self.operations[name] = operation.apply

    def run_operations(self, data: List[Any]) -> List[OperationResult]:
        results = []
        valid_data, invalid_data = self.validate_data(data)

        # 動的にスレッド数を調整
        max_workers = min(len(valid_data), 4)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {
                executor.submit(self.execute_operation, op_func, item): (item, name)
                for name, op_func in self.operations.items()
                for item in valid_data
            }

            for future in as_completed(future_to_item):
                item, operation_name = future_to_item[future]
                try:
                    result = future.result()
                    results.append(OperationResult(success=result))
                except Exception as e:
                    error_message = f"操作 '{operation_name}' でエラー: {str(e)}, データ: {item}"
                    results.append(OperationResult(error=error_message))

        self.visualize_results(results, invalid_data)
        return results

    def execute_operation(self, op_func: Callable[[Any], float], item: Any) -> float:
        return op_func(item)

    def validate_data(self, data: List[Any]) -> List[float]:
        valid = []
        invalid = []
        for item in data:
            if isinstance(item, (int, float)):
                valid.append(item)
            else:
                invalid.append(item)
        return valid, invalid

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        print("操作結果:")
        for result in results:
            if result.success is not None:
                print(f"成功: {result.success}")
            if result.error:
                print(f"エラー: {result.error}")

        if invalid_data:
            print("スキップされた無効なデータ:")
            for item in invalid_data:
                print(f"無効なデータ: {item}")

# 使用例
operation_manager = OperationManager()
operation_manager.register_operation("Increment", Increment())
operation_manager.register_operation("Cube", Cube())

data = [1, 2, 3, 'invalid', 4, 5] 
results = operation_manager.run_operations(data)
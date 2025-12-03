from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Dict, Optional, Tuple, Callable

class Operation:
    def apply(self, item: Any) -> Any:
        raise NotImplementedError("必ず派生クラスで実装してください。")

class Double(Operation):
    def apply(self, item: float) -> float:
        return item * 2

class Increment(Operation):
    def apply(self, item: float) -> float:
        return item + 1

class Square(Operation):
    def apply(self, item: float) -> float:
        return item ** 2

class OperationResult:
    def __init__(self, success: Optional[float] = None, error: Optional[str] = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self, max_workers: Optional[int] = None):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
        self.max_workers = max_workers or 4

    def register_operation(self, name: str, operation: Operation):
        self.operations[name] = operation.apply

    def run_operations(self, data: List[float]) -> List[OperationResult]:
        results = []
        valid_data = [item for item in data if isinstance(item, (int, float))]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_operation = {
                executor.submit(op_func, item): (item, name)
                for name, op_func in self.operations.items()
                for item in valid_data
            }

            for future in as_completed(future_to_operation):
                item, operation_name = future_to_operation[future]
                try:
                    result = future.result()
                    results.append(OperationResult(success=result))
                except Exception as e:
                    error_message = f"操作 '{operation_name}' でエラー: {str(e)}"
                    results.append(OperationResult(error=error_message))

        self.visualize_results(results)
        return results

    def visualize_results(self, results: List[OperationResult]):
        print("操作結果:")
        for result in results:
            if result.success is not None:
                print(f"成功: {result.success}")
            if result.error:
                print(f"エラー: {result.error}")

# 使用例
operation_manager = OperationManager()
operation_manager.register_operation("Double", Double())
operation_manager.register_operation("Increment", Increment())
operation_manager.register_operation("Square", Square())  # 新しい操作を登録

# 例のデータを使用してテスト
data = [1, 2, 3, 4, 5]
results = operation_manager.run_operations(data)
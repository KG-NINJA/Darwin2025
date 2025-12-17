from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Any, Optional

class Operation:
    def apply(self, item: float) -> float:
        raise NotImplementedError
    
    def name(self) -> str:
        return self.__class__.__name__

class Increment(Operation):
    def apply(self, item: float) -> float:
        return item + 1

class Cube(Operation):
    def apply(self, item: float) -> float:
        return item ** 3

class Square(Operation):
    def apply(self, item: float) -> float:
        return item ** 2

class OperationResult:
    def __init__(self, success: Optional[float] = None, error: Optional[str] = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], float]] = {}
    
    def register_operation(self, operation: Operation):
        self.operations[operation.name()] = operation.apply

    def run_operations(self, data: List[Any]) -> List[OperationResult]:
        results = []
        valid_data, invalid_data = self.validate_data(data)

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(op_func, item): (item, name)
                for name, op_func in self.operations.items()
                for item in valid_data
            }

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
            return OperationResult(error=f"操作 '{operation_name}' でエラー：{str(e)} (データ: {item})")

    def validate_data(self, data: List[Any]) -> (List[float], List[Any]):
        valid = [item for item in data if isinstance(item, (int, float))]
        invalid = [item for item in data if not isinstance(item, (int, float))]
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
operation_manager.register_operation(Increment())
operation_manager.register_operation(Cube())
operation_manager.register_operation(Square())

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data)
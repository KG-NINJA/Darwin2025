from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable, Any

class Operation:
    def apply(self, item: float) -> float:
        raise NotImplementedError

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
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}

    def register_operation(self, name: str, operation: Operation):
        self.operations[name] = operation.apply

    def run_operations(self, data: List[Any]) -> List[OperationResult]:
        results = []
        valid_data = self.validate_data(data)

        # 使用するスレッド数を動的に決定
        max_workers = min(len(valid_data), 4)  # スレッド数をデータ数に応じて調整
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
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
                    error_message = f"操作 '{operation_name}' でエラー: {str(e)}, データ: {item}"
                    results.append(OperationResult(error=error_message))

        # 結果の視覚化を改善
        self.visualize_results(results, invalid_data=data)
        return results

    def validate_data(self, data: List[Any]) -> List[float]:
        """データが数値であることを確認し、無効なデータを除外する。"""
        valid_data = []
        for item in data:
            if isinstance(item, (int, float)):
                valid_data.append(item)
            else:
                print(f"無効なデータタイプ: '{item}' はスキップされました。")
        return valid_data

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
                if not isinstance(item, (int, float)):
                    print(f"無効なデータ: {item}")

# 使用例
operation_manager = OperationManager()
operation_manager.register_operation("Double", Double())
operation_manager.register_operation("Increment", Increment())
operation_manager.register_operation("Square", Square())

# 例のデータを使用してテスト
data = [1, 2, 'invalid', 4, 5]  # 無効なデータが含まれている
results = operation_manager.run_operations(data)
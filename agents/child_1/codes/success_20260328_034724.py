from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Union

class Result:
    """結果を管理するクラス"""

    def __init__(self):
        self.successes = []
        self.errors = []

    def add_success(self, operation: str, item: Any, result: Any):
        self.successes.append((operation, item, result))

    def add_error(self, operation: str, item: Any, message: str):
        self.errors.append((operation, item, message))

    def to_dict(self) -> Dict[str, Union[List[str], List[str]]]:
        return {"successes": self.successes, "errors": self.errors}

class OperationManager:
    """操作管理クラス"""

    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = None) -> Dict[str, Any]:
        results = Result()
        max_workers = max_workers or len(data)  # デフォルトはデータ数に基づく

        def run_operation(item: Any, operation: Callable[[Any], Any], operation_name: str):
            """各操作を実行し、結果を返す"""
            try:
                result = operation(item)
                results.add_success(operation_name, item, result)
            except Exception as e:
                results.add_error(operation_name, item, self._generate_error_message(operation_name, item, str(e)))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(run_operation, item, self.operations[op_name], op_name): item
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                try:
                    future.result()
                except Exception as e:
                    results.add_error("Unknown", item, f"Unknown error: {str(e)}")

        return results.to_dict()

    def _generate_error_message(self, operation_name: str, item: Any, error: str) -> str:
        """エラーメッセージを生成する"""
        return f"操作 '{operation_name}' の実行中にエラーが発生しました。アイテム: {item}, エラー: {error}"

# 使用例
if __name__ == "__main__":
    manager = OperationManager()
    manager.register_operation("double", lambda x: x * 2)
    manager.register_operation("uppercase", lambda x: x.upper())
    result = manager.run_operations(["hello", 1, 2, 3], ["double", "uppercase"], max_workers=3)
    print(result)
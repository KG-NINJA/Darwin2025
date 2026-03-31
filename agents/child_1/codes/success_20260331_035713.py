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

class EnhancedOperationManager:
    """動的な操作を管理するクラス"""

    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = None) -> Dict[str, Any]:
        results = Result()
        max_workers = self._initialize_worker_count(max_workers, data)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._run_single_operation, item, op_name): item
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                self._handle_future_result(future, item, results)

        return results.to_dict()

    def _initialize_worker_count(self, max_workers: int, data: List[Any]) -> int:
        """最大ワーカー数を初期化"""
        return max_workers or len(data)

    def _run_single_operation(self, item: Any, operation_name: str):
        """単一の操作を実行し、結果を返す"""
        operation = self.operations[operation_name]
        try:
            result = operation(item)
            return (True, item, result)  # 成功
        except Exception as e:
            return (False, item, self._generate_error_message(operation_name, item, str(e)))

    def _handle_future_result(self, future, item: Any, results: Result):
        """Futureの結果を処理する"""
        try:
            success, item, result = future.result()
            if success:
                results.add_success(item, result)
            else:
                results.add_error(item, result)
        except Exception:
            results.add_error("Unknown", item, "未指定のエラーが発生しました。")

    def _generate_error_message(self, operation_name: str, item: Any, error: str) -> str:
        """エラーメッセージを生成する"""
        return f"操作 '{operation_name}' の実行中にエラーが発生しました。アイテム: {item}, エラー: {error}"

# 使用例
if __name__ == "__main__":
    manager = EnhancedOperationManager()
    manager.register_operation("double", lambda x: x * 2)
    manager.register_operation("uppercase", lambda x: x.upper())
    result = manager.run_operations(["hello", 1, 2, 3], ["double", "uppercase"], max_workers=3)
    print(result)
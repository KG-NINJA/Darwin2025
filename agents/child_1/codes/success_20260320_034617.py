from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Callable

class Result:
    """結果を管理するクラス"""
    def __init__(self):
        self.successes = []
        self.errors = []
        self.lock = Lock()

    def add_success(self, operation: str, item: Any, result: Any):
        with self.lock:
            self.successes.append((operation, item, result))

    def add_error(self, operation: str, item: Any, message: str):
        with self.lock:
            self.errors.append((operation, item, message))

    def to_dict(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "successes": self.successes,
                "errors": self.errors,
            }

class OperationManager:
    """拡張性のある操作管理クラス"""
    def __init__(self):
        self.operations = {}

    def register_operations(self, operations: Dict[str, Callable[[Any], Any]]) -> None:
        """複数の操作を関数として登録する"""
        self.operations.update(operations)

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> Dict[str, Any]:
        results = Result()

        def run_operation(item: Any, op_name: str):
            """各操作を実行し、結果を返す"""
            operation = self.operations.get(op_name)
            if operation is None:
                results.add_error(op_name, item, f"未登録の操作: '{op_name}' を指定されています。正しい操作名を使用してください。")
                return

            try:
                result = operation(item)
                results.add_success(op_name, item, result)
            except Exception as e:
                error_message = f"操作 '{op_name}' にてエラーが発生: {str(e)}"
                results.add_error(op_name, item, error_message)

        with ThreadPoolExecutor(max_workers=10) as executor:  # スレッド数を適切に管理
            futures = {executor.submit(run_operation, item, op_name): (item, op_name)
                       for item in data for op_name in chosen_operations}

            for future in as_completed(futures):
                future.result()

        return results.to_dict()
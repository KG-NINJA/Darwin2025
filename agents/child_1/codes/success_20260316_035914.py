from typing import Any, Dict, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class Result:
    """結果を管理するクラス"""
    def __init__(self):
        self.successes = []
        self.errors = []
        self.success_count = 0
        self.error_count = 0
        self.lock = Lock()  # スレッド安全のためのロック

    def add_success(self, operation: str, item: Any, result: Any):
        with self.lock:
            self.successes.append((operation, item, result))
            self.success_count += 1

    def add_error(self, operation: str, item: Any, message: str):
        with self.lock:
            self.errors.append((operation, item, message))
            self.error_count += 1

    def to_dict(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "successes": self.successes,
                "errors": self.errors,
                "success_count": self.success_count,
                "error_count": self.error_count
            }

    def clear_results(self):
        """結果をクリアするメソッド"""
        with self.lock:
            self.successes.clear()
            self.errors.clear()
            self.success_count = 0
            self.error_count = 0

class OperationManager:
    """拡張性のある操作管理クラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """操作を関数として登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> Dict[str, Any]:
        results = Result()

        def run_operation(item: Any, op_name: str):
            """各操作を実行し、結果を返す"""
            operation = self.operations.get(op_name)
            if operation:
                try:
                    result = operation(item)
                    results.add_success(op_name, item, result)
                except Exception as e:
                    error_message = f"エラー: {str(e)} (操作: {op_name}, アイテム: {item})"
                    results.add_error(op_name, item, error_message)
            else:
                results.add_error(op_name, item, f"未登録の操作: {op_name}")

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(run_operation, item, op_name): (item, op_name)
                       for item in data for op_name in chosen_operations}
            
            for future in as_completed(futures):
                future.result()

        return results.to_dict()

# 使用例
def double(item: int) -> int:
    return item * 2

def uppercase(item: str) -> str:
    return item.upper()

manager = OperationManager()
manager.register_operation("Double", double)
manager.register_operation("Uppercase", uppercase)
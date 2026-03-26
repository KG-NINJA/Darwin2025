from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Tuple, Union

class Result:
    """結果を管理するクラス"""
    def __init__(self):
        self.successes = []
        self.errors = []

    def add_success(self, operation: str, item: Any, result: Any):
        self.successes.append((operation, item, result))

    def add_error(self, operation: str, item: Any, message: str):
        self.errors.append((operation, item, message))

    def to_dict(self) -> Dict[str, Union[List[Tuple[str, Any, Any]], List[Tuple[str, Any, str]]]]:
        return {
            "successes": self.successes,
            "errors": self.errors,
        }

class OperationManager:
    """安定性向上の操作管理クラス"""
    def __init__(self, max_workers: int = 10):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
        self.max_workers = max_workers

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> Dict[str, Any]:
        results = Result()

        def run_operation(item: Any, operation: Callable[[Any], Any], operation_name: str):
            """各操作を実行し、結果を返す"""
            try:
                result = operation(item)
                results.add_success(operation_name, item, result)
            except Exception as e:
                error_message = self._generate_error_message(operation_name, item, str(e))
                results.add_error(operation_name, item, error_message)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(run_operation, item, self.operations[op_name], op_name): item
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                try:
                    future.result()  # わざとここで例外を取得
                except Exception as e:
                    error_message = self._generate_error_message("Unknown", item, str(e))
                    results.add_error("Unknown", item, error_message)

        return results.to_dict()

    def _generate_error_message(self, operation_name: str, item: Any, error: str) -> str:
        """より具体的なエラーメッセージを生成する"""
        return f"操作 '{operation_name}' の実行中にエラーが発生しました。アイテム: {item}, エラー: {error}"

# 使用例
if __name__ == "__main__":
    manager = OperationManager(max_workers=5)
    manager.register_operation("double", lambda x: x * 2)
    manager.register_operation("uppercase", lambda x: x.upper())
    result = manager.run_operations(["hello", 1, 2, 3], ["double", "uppercase"])
    print(result)
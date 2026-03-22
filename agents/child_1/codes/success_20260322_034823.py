from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Callable, Tuple

class Result:
    """結果を管理するクラス"""
    def __init__(self):
        self.successes = []
        self.errors = []

    def add_success(self, operation: str, item: Any, result: Any):
        self.successes.append((operation, item, result))

    def add_error(self, operation: str, item: Any, message: str):
        self.errors.append((operation, item, message))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "successes": self.successes,
            "errors": self.errors,
        }

class Operation:
    """操作を表す基本クラス"""
    def execute(self, item: Any) -> Any:
        raise NotImplementedError("このメソッドはサブクラスで実装してください。")

class DoubleOperation(Operation):
    def execute(self, item: Any) -> Any:
        return item * 2

class UppercaseOperation(Operation):
    def execute(self, item: Any) -> Any:
        return item.upper()

class OperationManager:
    """拡張性のある操作管理クラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        """単一の操作を関数として登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> Dict[str, Any]:
        results = Result()

        def run_operation(item: Any, operation: Operation):
            """各操作を実行し、結果を返す"""
            try:
                result = operation.execute(item)
                results.add_success(operation.__class__.__name__, item, result)
            except Exception as e:
                error_message = f"操作 '{operation.__class__.__name__}' にてエラーが発生: {str(e)}"
                results.add_error(operation.__class__.__name__, item, error_message)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(run_operation, item, self.operations[op_name]): (item, op_name)
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                future.result()

        return results.to_dict()
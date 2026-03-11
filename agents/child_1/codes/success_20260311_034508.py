from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Protocol, TypeVar, Any, List, Dict
import threading

T = TypeVar('T')

class Operation(Protocol[T]):
    """操作を定義するインターフェース"""
    def execute(self, item: T) -> Any:
        pass

class ConcreteOperationA(Operation[int]):
    """数値を2倍にする操作"""
    def execute(self, item: int) -> int:
        return item * 2

class ConcreteOperationB(Operation[str]):
    """文字列を大文字にする操作"""
    def execute(self, item: str) -> str:
        return item.upper()

class Result:
    """結果管理用クラス"""
    def __init__(self):
        self.success: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.lock = threading.Lock()  # 排他制御のためのロック

    def add_success(self, operation: str, input_item: Any, result: Any):
        with self.lock:
            self.success.append({
                "operation": operation,
                "input": input_item,
                "result": result
            })

    def add_error(self, operation: str, input_item: Any, error_msg: str):
        with self.lock:
            self.errors.append({
                "operation": operation,
                "input": input_item,
                "error": error_msg
            })

    def to_dict(self) -> Dict[str, Any]:
        return {"success": self.success, "errors": self.errors}

class OperationManager:
    """操作を管理するクラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> Dict[str, Any]:
        """選択した操作を並列に実行し、それぞれの結果を管理する"""
        results = Result()

        def run_operation(item: Any, op_name: str):
            """各操作を実行し、結果を返す"""
            operation = self.operations.get(op_name)
            if operation:
                try:
                    result = operation.execute(item)
                    results.add_success(op_name, item, result)
                except Exception as e:
                    results.add_error(op_name, item, f"エラー: {str(e)} (操作: {op_name})")
            else:
                results.add_error(op_name, item, f"未登録の操作: {op_name}")

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(run_operation, item, op_name): (item, op_name)
                       for item in data for op_name in chosen_operations}
            
            for future in as_completed(futures):
                future.result()

        return results.to_dict()

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
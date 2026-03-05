from typing import Protocol, TypeVar, List, Any, Dict

T = TypeVar('T')

class Operation(Protocol[T]):
    """操作を定義するインターフェース"""
    def execute(self, item: T) -> dict:
        ...

class ConcreteOperationA:
    """整数を2倍にする操作"""
    def execute(self, item: int) -> Dict[str, Any]:
        return {"result": item * 2, "error": None}

class ConcreteOperationB:
    """文字列を大文字にする操作"""
    def execute(self, item: str) -> Dict[str, Any]:
        return {"result": item.upper(), "error": None}

class OperationManager:
    """操作を管理するクラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> dict:
        """選択した操作を実行し、それぞれの結果を管理する"""
        overall_results = {"operations": {}}
        
        for item in data:
            operation_results = {}
            for op_name in chosen_operations:
                operation = self.operations.get(op_name)
                if operation:
                    try:
                        result = operation.execute(item)
                        operation_results[op_name] = {
                            "result": result["result"],
                            "error": result["error"]
                        }
                    except Exception as e:
                        operation_results[op_name] = {
                            "result": None,
                            "error": f"エラー: {e} (操作名: {op_name})"
                        }
                else:
                    operation_results[op_name] = {
                        "result": None,
                        "error": f"未登録の操作: {op_name}"
                    }
            overall_results["operations"][item] = operation_results
        
        return overall_results

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
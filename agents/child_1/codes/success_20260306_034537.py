from typing import Protocol, TypeVar, List, Any

T = TypeVar('T')

class Operation(Protocol[T]):
    """操作を定義するインターフェース"""
    def execute(self, item: T) -> Any:
        ...

class ConcreteOperationA:
    """整数を2倍にする操作"""
    def execute(self, item: int) -> int:
        return item * 2

class ConcreteOperationB:
    """文字列を大文字にする操作"""
    def execute(self, item: str) -> str:
        return item.upper()

class OperationManager:
    """操作を管理するクラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> dict:
        """選択した操作を実行し、それぞれの結果を管理する"""
        overall_results = {"success": [], "errors": []}
        
        for item in data:
            for op_name in chosen_operations:
                operation = self.operations.get(op_name)
                if operation:
                    try:
                        result = operation.execute(item)
                        overall_results["success"].append({
                            "operation": op_name,
                            "input": item,
                            "result": result
                        })
                    except Exception as e:
                        overall_results["errors"].append({
                            "operation": op_name,
                            "input": item,
                            "error": f"エラー: {e} (操作名: {op_name})"
                        })
                else:
                    overall_results["errors"].append({
                        "operation": op_name,
                        "input": item,
                        "error": f"未登録の操作: {op_name}"
                    })
        
        return overall_results

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
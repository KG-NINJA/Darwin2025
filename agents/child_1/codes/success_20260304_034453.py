from typing import Protocol, TypeVar, List, Any

T = TypeVar('T')

class Operation(Protocol[T]):
    """操作を定義するインターフェース"""
    def execute(self, item: T) -> dict:
        ...

class ConcreteOperationA:
    """整数を2倍にする操作"""
    def execute(self, item: int) -> dict:
        return {"results": [item * 2], "errors": []}

class ConcreteOperationB:
    """文字列を大文字にする操作"""
    def execute(self, item: str) -> dict:
        return {"results": [item.upper()], "errors": []}

class OperationManager:
    """操作を管理するクラス"""
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> dict:
        """選択した操作を実行し、結果とエラーを管理する"""
        overall_results = {"results": [], "errors": []}
        
        for item in data:
            operation_results = {"results": [], "errors": []}
            for op_name in chosen_operations:
                operation = self.operations.get(op_name)
                if operation:
                    try:
                        result = operation.execute(item)
                        operation_results['results'].extend(result['results'])
                        operation_results['errors'].extend(result['errors'])
                    except Exception as e:
                        operation_results['errors'].append(f"エラー: {e} (操作名: {op_name})")
                else:
                    operation_results['errors'].append(f"未登録の操作: {op_name}")
                    
            # 全体の結果に操作毎の結果を追加
            overall_results['results'].extend(operation_results['results'])
            overall_results['errors'].extend(operation_results['errors'])
        
        return overall_results

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
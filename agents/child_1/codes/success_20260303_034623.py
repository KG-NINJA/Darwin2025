from typing import Protocol, TypeVar, List, Any

T = TypeVar('T')

class Operation(Protocol[T]):
    def execute(self, item: T) -> dict:
        ...

class ConcreteOperationA:
    def execute(self, item: int) -> dict:
        return {"results": [item * 2], "errors": []}

class ConcreteOperationB:
    def execute(self, item: str) -> dict:
        return {"results": [item.upper()], "errors": []}

class OperationManager:
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Operation) -> None:
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        
        for item in data:
            for op_name in chosen_operations:
                operation = self.operations.get(op_name)
                if operation:
                    try:
                        result = operation.execute(item)
                        results['results'].extend(result['results'])
                        if result['errors']:
                            results['errors'].extend(result['errors'])
                    except Exception as e:
                        results['errors'].append(f"エラー: {e} (操作名: {op_name})")
                else:
                    results['errors'].append(f"未登録の操作: {op_name}")
                    
        return results

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
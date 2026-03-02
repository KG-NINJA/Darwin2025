from typing import Protocol, TypeVar, Any

T = TypeVar('T')

class Operation(Protocol[T]):
    def execute(self, item: T) -> dict:
        ...

class ConcreteOperationA:
    def execute(self, item: int) -> dict:
        # 任意の操作を実装
        return {"results": [item * 2], "errors": []}

class ConcreteOperationB:
    def execute(self, item: str) -> dict:
        # 任意の操作を実装
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
                    result = operation.execute(item)
                    results['results'].extend(result['results'])
                    results['errors'].extend(result['errors'])
                else:
                    results['errors'].append(f"未登録の操作: {op_name}")
        return results

# 使用例
manager = OperationManager()
manager.register_operation("Double", ConcreteOperationA())
manager.register_operation("Uppercase", ConcreteOperationB())
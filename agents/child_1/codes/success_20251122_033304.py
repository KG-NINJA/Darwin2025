from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Dict


class Operation:
    """操作を表す基本クラス"""
    def apply(self, item):
        raise NotImplementedError("必ず派生クラスで実装してください。")

    def configure(self, *args, **kwargs):
        """操作の構成を設定するためのメソッド"""
        pass


class Double(Operation):
    def apply(self, item):
        return item * 2

    
class Increment(Operation):
    def apply(self, item):
        return item + 1

    
class OperationManager:
    """操作を管理するクラス"""
    def __init__(self):
        self.operations: Dict[str, Operation] = {}

    def register_operation(self, name: str, operation: Operation):
        """操作を登録"""
        self.operations[name] = operation

    def run_operations(self, data: List[float]) -> List[float]:
        """登録された全ての操作をデータに適用"""
        results = []
        errors = []
        
        with ThreadPoolExecutor(max_workers=len(self.operations)) as executor:
            future_to_operation = {executor.submit(op.apply, item): (item, name)
                                    for name, op in self.operations.items() 
                                    for item in data}

            for future in as_completed(future_to_operation):
                item, operation_name = future_to_operation[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    error_message = f"エラー発生 - 操作: {operation_name} | アイテム: {item} | メッセージ: {e}"
                    errors.append(error_message)

        if errors:
            for error in errors:
                print(error)

        return results
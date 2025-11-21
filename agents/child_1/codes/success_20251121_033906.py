from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any

class Operation:
    """操作を表す基本クラス"""
    def apply(self, item):
        raise NotImplementedError("必ず派生クラスで実装してください。")

class Double(Operation):
    def apply(self, item):
        return item * 2

class Square(Operation):
    def apply(self, item):
        return item ** 2

class Increment(Operation):
    def apply(self, item):
        return item + 1

class Multiply(Operation):
    def __init__(self, factor):
        self.factor = factor

    def apply(self, item):
        return item * self.factor

def validate_numerical_input(data: List[Any]) -> None:
    """入力データに対する検証"""
    if not all(isinstance(item, (int, float)) for item in data):
        raise ValueError("全ての要素は数値でなければなりません。")

def apply_operations(data: List[float], operations: List[Operation]) -> List[float]:
    """指定された操作をデータに適用"""
    validate_numerical_input(data)
    
    # 無効なデータは全て除外
    valid_data = [item for item in data if isinstance(item, (int, float)) and item > 0]

    results = []
    errors = []
    
    # 使用するスレッド数をデータ長で制限
    num_workers = min(len(valid_data), len(operations))

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_item = {executor.submit(operation.apply, item): (item, operation.__class__.__name__) 
                           for item in valid_data for operation in operations}

        for future in as_completed(future_to_item):
            item, operation_name = future_to_item[future]
            try:
                results.append(future.result())
            except Exception as e:
                error_message = f"エラー発生 - 操作: {operation_name} | アイテム: {item} | メッセージ: {e}"
                errors.append(error_message)

    if errors:
        for error in errors:
            print(error)

    return results
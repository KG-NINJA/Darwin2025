from concurrent.futures import ThreadPoolExecutor, as_completed

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

def validate_numerical_input(data):
    """入力データに対する検証"""
    if not isinstance(data, list):
        raise ValueError("データはリストである必要があります。")
    if any(not isinstance(item, (int, float)) for item in data):
        raise ValueError("リストには数値以外の要素が含まれていることができません。")

def apply_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_numerical_input(data)

    # 有効な数値のみを抽出（負の数とゼロを除外）
    valid_data = [item for item in data if isinstance(item, (int, float)) and item > 0]

    results = []
    errors = []
    # 使用するスレッド数を指定
    num_workers = min(len(operations), len(valid_data))

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_operation = {executor.submit(operation.apply, item): (operation, item) 
                                for item in valid_data for operation in operations}
        
        for future in as_completed(future_to_operation):
            operation, item = future_to_operation[future]
            try:
                results.append(future.result())
            except Exception as e:
                errors.append(f"エラー発生 - {operation.__class__.__name__} on item {item}: {e}")

    if errors:
        for error in errors:
            print(error)

    return results
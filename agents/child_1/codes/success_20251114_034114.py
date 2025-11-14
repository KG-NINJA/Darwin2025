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
    """新しいMultiply操作の追加"""
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
    valid_data = list(filter(lambda item: isinstance(item, (int, float)) and item > 0, data))

    # 操作を動的に適用
    results = []
    for operation in operations:
        results.extend(operation.apply(item) for item in valid_data)
    
    return results
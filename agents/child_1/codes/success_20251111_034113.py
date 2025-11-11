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

def apply_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_numerical_input(data)

    # 有効な数値のみを抽出（負の数とゼロを除外）
    valid_data = [item for item in data if isinstance(item, (int, float)) and item > 0]

    # 各操作を適用し、結果を一度のリスト合成で取得
    return [result for item in valid_data for operation in operations for result in [operation.apply(item)]]
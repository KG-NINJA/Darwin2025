def validate_input(data):
    """入力データの妥当性を検証"""
    if not all(isinstance(i, (int, float)) for i in data):
        raise ValueError("すべての要素は数値である必要があります。")

def double_operation(data):
    """データを2倍にする操作"""
    validate_input(data)
    return [item * 2 for item in data if item > 0]

def square_operation(data):
    """データを二乗する操作"""
    validate_input(data)
    return [item ** 2 for item in data if item > 0]

def increment_operation(data):
    """データを1つ増やす操作"""
    validate_input(data)
    return [item + 1 for item in data if item > 0]
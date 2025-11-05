def validate_numerical_input(data):
    """入力データの妥当性を確認し、エラーをスロー"""
    if not isinstance(data, list):
        raise ValueError("入力はリストである必要があります。")
    if not all(isinstance(i, (int, float)) for i in data):
        raise ValueError("すべての要素は数値である必要があります。")

def double(item): return item * 2
def square(item): return item ** 2
def increment(item): return item + 1

operation_map = {
    "double": double,
    "square": square,
    "increment": increment
}

def apply_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_numerical_input(data)
    
    results = []
    for item in data:
        if item <= 0:  # 負の値は無視
            continue
        for operation in operations:
            if operation not in operation_map:
                raise ValueError(f"無効な操作: {operation}")
            results.append(operation_map[operation](item))

    return results
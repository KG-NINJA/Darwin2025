def validate_numerical_input(data):
    """入力データの妥当性を確認し、エラーをスロー"""
    if not all(isinstance(i, (int, float)) for i in data):
        raise ValueError("すべての要素は数値である必要があります。創造的なデータを使用してください。")

def apply_operation(item, operation):
    """指定された操作を要素に適用"""
    if operation == "double":
        return item * 2
    elif operation == "square":
        return item ** 2
    elif operation == "increment":
        return item + 1
    else:
        raise ValueError(f"無効な操作: {operation}")

def process_with_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_numerical_input(data)

    results = []
    for operation in operations:
        results.extend(apply_operation(item, operation) for item in data if item > 0)

    return results
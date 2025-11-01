def validate_input(data):
    """入力データの妥当性を検証"""
    if not all(isinstance(i, (int, float)) for i in data):
        raise ValueError("すべての要素は数値である必要があります。")

def process_with_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_input(data)

    results = []
    for operation in operations:
        if operation == "double":
            results += [item * 2 for item in data if item > 0]
        elif operation == "square":
            results += [item ** 2 for item in data if item > 0]
        elif operation == "increment":
            results += [item + 1 for item in data if item > 0]
    
    return results
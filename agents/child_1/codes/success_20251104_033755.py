def validate_numerical_input(data):
    """入力データの妥当性を確認し、エラーをスロー"""
    if not isinstance(data, list):
        raise ValueError("入力はリストである必要があります。")
    if not all(isinstance(i, (int, float)) for i in data):
        raise ValueError("すべての要素は数値である必要があります。")

def double(item): return item * 2
def square(item): return item ** 2
def increment(item): return item + 1

# 操作と対応する関数の辞書
operation_map = {
    "double": double,
    "square": square,
    "increment": increment
}

def apply_operation(item, operation):
    """指定された操作を要素に適用"""
    if operation not in operation_map:
        raise ValueError(f"無効な操作: {operation}")
    return operation_map[operation](item)

def process_with_operations(data, operations):
    """指定された操作をデータに適用"""
    validate_numerical_input(data)

    results = []  # 結果を格納するリスト
    for operation in operations:
        try:
            results.extend(apply_operation(item, operation) for item in data if item > 0)
        except Exception as e:
            print(f"操作 '{operation}' の適用中にエラー: {str(e)}")

    return results
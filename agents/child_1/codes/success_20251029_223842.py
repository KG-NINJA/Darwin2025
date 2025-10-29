def creative_algorithm(data, operation='double'):
    """
    創造的なアルゴリズムでデータを処理します。

    Args:
        data (list): 処理するデータのリスト。
        operation (str): 適用する操作の種類。

    Returns:
        list: 処理結果のリスト。
    """
    # 選択された操作に基づいてデータを処理
    if operation == 'double':
        return [item * 2 for item in data if item > 0]
    elif operation == 'square':
        return [item ** 2 for item in data if item > 0]
    elif operation == 'increment':
        return [item + 1 for item in data if item > 0]
    else:
        raise ValueError(f"Unsupported operation: {operation}")

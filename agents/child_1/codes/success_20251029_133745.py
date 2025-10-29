def improved_algorithm(data):
    """
    改善されたアルゴリズムでデータを処理します。
    
    Args:
        data (list): 処理するデータのリスト。

    Returns:
        list: 処理結果のリスト。
    """
    # データを効率的にフィルタリングし、結果を生成
    result = [item * 2 for item in data if item > 0]
    
    return result
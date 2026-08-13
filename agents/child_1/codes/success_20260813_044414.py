from typing import Callable, Dict, Any, List

class EfficientDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Callable[[Any], Dict[str, Any]]] = {}
    
    def add_strategy(self, name: str, strategy: Callable[[Any], Dict[str, Any]]):
        """戦略を追加します。"""
        if name in self.strategies:
            return self._log_error(f"戦略 '{name}' はすでに存在します。")
        
        if not callable(strategy):
            return self._log_error("渡された戦略は呼び出し可能である必要があります。")
        
        self.strategies[name] = strategy
        print(f"戦略 '{name}' が追加されました。")

    def execute_strategy(self, strategy_name: str, data: Any) -> Dict[str, Any]:
        """指定した戦略を実行します。"""
        strategy = self.strategies.get(strategy_name)

        if not strategy:
            return self._log_error(f"指定された戦略 '{strategy_name}' は存在しません。")

        if not isinstance(data, list):
            return self._log_error("データはリスト型でなければなりません。引数のタイプをご確認ください。")
        
        try:
            return strategy(data)
        except Exception as e:
            return self._log_error(f"エラーが発生しました: {str(e)}")

    def _log_error(self, message: str) -> Dict[str, Any]:
        """エラーメッセージを出力し、辞書形式で返却します。"""
        print(f"[ERROR] {message}")
        return {'error': message}

def mean_strategy(data: List[float]) -> Dict[str, float]:
    """平均値を計算する戦略。"""
    if not data:
        return {'error': "データが空です。"}
    return {'mean': sum(data) / len(data)}

def median_strategy(data: List[float]) -> Dict[str, float]:
    """中央値を計算する戦略。"""
    if not data:
        return {'error': "データが空です。"}
    sorted_data = sorted(data)
    mid = len(sorted_data) // 2
    return {
        'median': (sorted_data[mid - 1] + sorted_data[mid]) / 2 if len(sorted_data) % 2 == 0 else sorted_data[mid]
    }

async def main():
    data_processor = EfficientDataProcessor()
    data_processor.add_strategy('mean', mean_strategy)
    data_processor.add_strategy('median', median_strategy)

    print("利用可能な戦略:", list(data_processor.strategies.keys()))

    results_mean = data_processor.execute_strategy('mean', [1, 2, 3, 4, 5])
    results_median = data_processor.execute_strategy('median', [1, 2, 3, 4, 5])
    
    print("Mean結果:", results_mean)
    print("Median結果:", results_median)

# asyncio.run(main())
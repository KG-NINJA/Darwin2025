from typing import Callable, Dict, Any, List
from collections import defaultdict

class FlexibleDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Callable[[Any], Dict[str, Any]]] = defaultdict(lambda: None)

    def add_strategy(self, name: str, strategy: Callable[[Any], Dict[str, Any]]):
        """戦略を追加します。"""
        if name in self.strategies:
            print(f"戦略 '{name}' はすでに存在します。")
        else:
            self.strategies[name] = strategy
            print(f"戦略 '{name}' が追加されました。")

    def execute_strategy(self, strategy_name: str, data: Any) -> Dict[str, Any]:
        """指定した戦略を実行します。"""
        if strategy_name not in self.strategies or self.strategies[strategy_name] is None:
            return {'error': f"指定された戦略 '{strategy_name}' は存在しません。"}

        if not isinstance(data, list):
            return {'error': "データはリスト型でなければなりません。引数のタイプをご確認ください。"}
        
        try:
            return self.strategies[strategy_name](data)
        except Exception as e:
            return {'error': f"エラーが発生しました: {str(e)}"}

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
    data_processor = FlexibleDataProcessor()
    data_processor.add_strategy('mean', mean_strategy)
    data_processor.add_strategy('median', median_strategy)

    print("利用可能な戦略:", list(data_processor.strategies.keys()))

    results_mean = data_processor.execute_strategy('mean', [1, 2, 3, 4, 5])
    results_median = data_processor.execute_strategy('median', [1, 2, 3, 4, 5])
    
    print("Mean結果:", results_mean)
    print("Median結果:", results_median)

# asyncio.run(main())
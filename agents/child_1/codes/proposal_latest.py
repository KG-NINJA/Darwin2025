from typing import Callable, Dict, Any
from collections import defaultdict

class FlexibleDataProcessor:
    def __init__(self):
        # 戦略を保持するための辞書
        self.strategies: Dict[str, Callable[[Any], Dict[str, Any]]] = defaultdict(lambda: None)

    def add_strategy(self, name: str, strategy: Callable[[Any], Dict[str, Any]]):
        """新しい戦略を追加するメソッド"""
        self.strategies[name] = strategy

    def execute_strategy(self, strategy_name: str, data: Any) -> Dict[str, Any]:
        """特定の戦略を実行するメソッド"""
        if strategy_name not in self.strategies or self.strategies[strategy_name] is None:
            return {'error': f"指定された戦略 '{strategy_name}' は存在しません。"}
        
        return self.strategies[strategy_name](data)

# 例としての戦略
def mean_strategy(data: List[float]) -> Dict[str, float]:
    if not data:
        return {'error': "データが空です。"}
    return {'mean': sum(data) / len(data)}

def median_strategy(data: List[float]) -> Dict[str, float]:
    if not data:
        return {'error': "データが空です。"}
    sorted_data = sorted(data)
    mid = len(sorted_data) // 2
    return {
        'median': (sorted_data[mid - 1] + sorted_data[mid]) / 2 if len(sorted_data) % 2 == 0 else sorted_data[mid]
    }

# main関数の例
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
import asyncio
from typing import Any, Dict, List

class Strategy:
    """ストラテジーパターンの基底クラス"""
    def execute(self, data: List[Any]) -> Dict[str, Any]:
        raise NotImplementedError("このメソッドはサブクラスで実装される必要があります。")

class StatisticsStrategy(Strategy):
    """統計情報を計算するための戦略クラス"""
    def execute(self, data: List[float]) -> Dict[str, Any]:
        if not data:
            return {'error': "データが空です。"}
        if any(not isinstance(x, (int, float)) for x in data):
            return {'error': "データは数値である必要があります。"}
        stats = {'sum': sum(data), 'count': len(data), 'average': sum(data) / len(data)}
        return stats

class DataProcessor:
    def __init__(self):
        self.strategies = {}

    def register_strategy(self, name: str, strategy: Strategy):
        """指定した戦略を登録する関数"""
        self.strategies[name] = strategy

    def get_strategy(self, strategy_name: str) -> Strategy:
        """戦略名に基づいて戦略を取得する関数"""
        if strategy_name not in self.strategies:
            raise ValueError(f"無効な戦略名 '{strategy_name}' が指定されました。")
        return self.strategies[strategy_name]

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、指定した戦略名に基づいて結果を返す関数"""
        try:
            strategy = self.get_strategy(strategy_name)
            result = await asyncio.to_thread(strategy.execute, data)
            return result
        except ValueError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': "予期しないエラーが発生しました。"}

# 使用例
data_processor = DataProcessor()
data_processor.register_strategy('statistics', StatisticsStrategy())

async def main():
    results = await data_processor.process_data([1, 2, '3', 4.0, 5], strategy_name='statistics')
    print(results)

# asyncio.run(main())
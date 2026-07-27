from typing import List, Dict, Any
import asyncio

class Strategy:
    """抽象戦略クラス"""
    
    async def execute(self, data: List[float]) -> Dict[str, Any]:
        raise NotImplementedError("戦略においてexecuteメソッドを実装する必要があります。")

class StatisticsStrategy(Strategy):
    async def execute(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {'error': "データが空です。"}
        return {
            'mean': sum(data) / len(data),
            'sum': sum(data)
        }

class MedianStrategy(Strategy):
    async def execute(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {'error': "データが空です。"}
        sorted_data = sorted(data)
        mid = len(sorted_data) // 2
        return {
            'median': (sorted_data[mid - 1] + sorted_data[mid]) / 2 if len(sorted_data) % 2 == 0 else sorted_data[mid]
        }

class StableDataProcessor:
    """データの安定処理クラス"""
    
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}

    def add_strategy(self, name: str, strategy: Strategy):
        """戦略を追加する"""
        self.strategies[name] = strategy

    async def process_data(self, data: List[float], strategy_name: str) -> Dict[str, Any]:
        if strategy_name not in self.strategies:
            return {'error': f"指定された戦略名 '{strategy_name}' は無効です。"}
        
        try:
            self.validate_data(data)
            result = await self.strategies[strategy_name].execute(data)
            return result
        except ValueError as e:
            return {'error': f"バリデーションエラー: {str(e)}"}
        except Exception as e:
            return {'error': f"予期しないエラーが発生しました: {str(e)}"}

    def validate_data(self, data: List[float]):
        if not data:
            raise ValueError("データを入力してください。リストが空です。")
        if any(not isinstance(x, (int, float)) for x in data):
            raise ValueError("全てのデータは数値である必要があります。")

# 使用例
data_processor = StableDataProcessor()
data_processor.add_strategy('statistics', StatisticsStrategy())
data_processor.add_strategy('median', MedianStrategy())

async def main():
    try:
        results_stats = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='statistics')
        results_median = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='median')
        print(results_stats)
        print(results_median)
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

# asyncio.run(main())
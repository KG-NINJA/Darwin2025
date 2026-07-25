from typing import List, Dict, Any, Callable

class StableDataProcessor:
    """データの安定処理クラス"""
    
    def __init__(self):
        self.strategies: Dict[str, Callable[[List[Any]], Dict[str, Any]]] = {}

    def add_strategy(self, name: str, strategy: Callable[[List[Any]], Dict[str, Any]]):
        """戦略を追加する"""
        self.strategies[name] = strategy

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、結果を返します"""
        if strategy_name not in self.strategies:
            return {'error': f"指定された戦略名 '{strategy_name}' は無効です。"}
        
        try:
            self.validate_data(data)
            result = await self.strategies[strategy_name](data)
            return result
        except ValueError as e:
            return {'error': f"バリデーションエラー: {str(e)}"}
        except Exception as e:
            return {'error': "予期しないエラーが発生しました。"}

    def validate_data(self, data: List[Any]):
        """データの検証を行う"""
        if not data:
            raise ValueError("データを入力してください。リストが空です。")
        if any(not isinstance(x, (int, float)) for x in data):
            raise ValueError("全てのデータは数値である必要があります。")

async def process_statistics(data: List[float]) -> Dict[str, float]:
    """統計データを処理する戦略"""
    if not data:
        return {'mean': 0, 'sum': 0}

    return {
        'mean': sum(data) / len(data),
        'sum': sum(data)
    }

async def process_median(data: List[float]) -> Dict[str, float]:
    """中央値を計算する戦略"""
    sorted_data = sorted(data)
    mid = len(sorted_data) // 2
    if len(sorted_data) % 2 == 0:
        median = (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        median = sorted_data[mid]
    
    return {
        'median': median
    }

# 使用例
data_processor = StableDataProcessor()
data_processor.add_strategy('statistics', process_statistics)
data_processor.add_strategy('median', process_median)

async def main():
    results_stats = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='statistics')
    results_median = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='median')
    print(results_stats)
    print(results_median)

# asyncio.run(main())
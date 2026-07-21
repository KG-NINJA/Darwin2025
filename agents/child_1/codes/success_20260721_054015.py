import asyncio
from typing import Any, Dict, List, Callable

class StableDataProcessor:
    """安定性を高めたデータプロセッサ"""

    def __init__(self):
        self.strategies = {}

    def add_strategy(self, name: str, strategy: Callable[[List[float]], Dict[str, Any]]):
        """新しい戦略を追加する"""
        self.strategies[name] = strategy

    def validate_data(self, data: List[Any]):
        """データの検証を行い、エラーを返す"""
        if not data:
            raise ValueError("データが空です。")
        if any(not isinstance(x, (int, float)) for x in data):
            raise ValueError("データは数値である必要があります。")

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、指定した戦略名に基づいて結果を返す関数"""
        if strategy_name not in self.strategies:
            return {'error': f"無効な戦略名 '{strategy_name}' が指定されました。"}
        
        try:
            # データを検証する
            self.validate_data(data)
            result = await self.strategies[strategy_name](data)
            return result
        except ValueError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': "予期しないエラーが発生しました。"}

async def process_statistics(data: List[float]) -> Dict[str, Any]:
    """統計情報を非同期に処理し、計算結果を返す関数"""
    return {
        'sum': sum(data),
        'count': len(data),
        'average': sum(data) / len(data)
    }

# 使用例
data_processor = StableDataProcessor()
data_processor.add_strategy('statistics', process_statistics)

async def main():
    results = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='statistics')
    print(results)

# asyncio.run(main())
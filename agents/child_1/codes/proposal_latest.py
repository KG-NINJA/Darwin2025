from typing import List, Dict, Any

class StableDataProcessor:
    """データの安定処理クラス"""
    
    def __init__(self):
        self.strategies = {}

    def add_strategy(self, name: str, strategy):
        """戦略を追加する"""
        self.strategies[name] = strategy

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、結果を返します"""
        if strategy_name not in self.strategies:
            return {'error': f"指定された戦略名 '{strategy_name}' は無効です。"}
        
        try:
            # 検証と処理を行う
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
            raise ValueError("エラー: すべてのデータは数値である必要があります。")

# 使用例
data_processor = StableDataProcessor()
data_processor.add_strategy('statistics', process_statistics)

async def main():
    results = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='statistics')
    print(results)

# asyncio.run(main())
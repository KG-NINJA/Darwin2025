class IntuitiveDataProcessor(StableDataProcessor):
    """直感的なデータプロセッサ"""

    def validate_data(self, data: List[Any]):
        """データの検証を行い、エラーメッセージをユーザーに理解しやすくする"""
        if not data:
            raise ValueError("データを入力してください。リストが空です。")
        if any(not isinstance(x, (int, float)) for x in data):
            raise ValueError("エラー: すべてのデータは数値である必要があります。")

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し結果を返します"""
        if strategy_name not in self.strategies:
            return {'error': f"指定された戦略名 '{strategy_name}' は無効です。可能な戦略を確認してください。"}
        
        try:
            # 検証と処理を行う
            self.validate_data(data)
            result = await self.strategies[strategy_name](data)
            return result
        except ValueError as e:
            return {'error': f"バリデーションエラー: {str(e)}"}
        except Exception as e:
            return {'error': "予期しないエラーが発生しました。お手数ですが、再度お試しください。"}

# 使用例
intuitive_processor = IntuitiveDataProcessor()
intuitive_processor.add_strategy('statistics', process_statistics)

async def main():
    results = await intuitive_processor.process_data([], strategy_name='statistics')
    print(results)  # エラーメッセージを確認

# asyncio.run(main())
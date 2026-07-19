import asyncio
from typing import Any, Dict, List

class EfficientDataProcessor:
    """効率的データプロセッサ"""
    
    def validate_data(self, data: List[Any]):
        """データの検証を行い、エラーを返す"""
        if not data:
            raise ValueError("データが空です。")
        if any(not isinstance(x, (int, float)) for x in data):
            raise ValueError("データは数値である必要があります。")

    async def process_statistics(self, data: List[float]) -> Dict[str, Any]:
        """統計情報を非同期に処理し、計算結果を返す関数"""
        self.validate_data(data)
        return {
            'sum': sum(data),
            'count': len(data),
            'average': sum(data) / len(data)
        }

    async def process_data(self, data: List[Any], strategy_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、指定した戦略名に基づいて結果を返す関数"""
        try:
            if strategy_name == 'statistics':
                return await self.process_statistics(data)
            else:
                raise ValueError(f"無効な戦略名 '{strategy_name}' が指定されました。")
        except ValueError as e:
            return {'error': str(e)}
        except Exception as e:
            return {'error': "予期しないエラーが発生しました。"}

# 使用例
data_processor = EfficientDataProcessor()

async def main():
    results = await data_processor.process_data([1, 2, 3.5, 4.0, 5], strategy_name='statistics')
    print(results)

# asyncio.run(main())
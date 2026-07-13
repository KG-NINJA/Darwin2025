import asyncio
from typing import List, Dict, Any, Callable
from functools import lru_cache

class DataProcessor:
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Callable[[List[Any]], Dict[str, Any]]):
        """指定した操作を登録する関数"""
        if name in self.operations:
            raise ValueError(f"操作名 '{name}' はすでに登録されています。")
        self.operations[name] = operation

    @lru_cache(maxsize=128)  # メモリを効率的に管理
    async def process_data(self, data: List[Any], operation_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、指定した操作名に基づいて結果を返す関数"""
        if operation_name not in self.operations:
            return {'error': f"無効な操作名 '{operation_name}' が指定されました。"}
        
        if not data:
            return {'error': "データセットは空です。"}
        
        try:
            # スレッドを効果的に使用
            result = await asyncio.to_thread(self.operations[operation_name], data)
            return result
        except Exception as e:
            return {'error': f"処理中にエラーが発生しました: {str(e)}"}

async def calculate_statistics(data: List[float]) -> Dict[str, Any]:
    """データの統計情報（合計と平均）を計算する関数"""
    if not data:
        return {'error': "データが空です。"}
    stats = {'sum': sum(data), 'count': len(data), 'average': sum(data)/len(data)}
    return stats

# 使用例
data_processor = DataProcessor()
data_processor.register_operation('statistics', calculate_statistics)

async def main():
    results = await data_processor.process_data([1, 2, 3, 4, 5], operation_name='statistics')
    print(results)

# asyncio.run(main())
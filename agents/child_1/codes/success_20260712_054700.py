import asyncio
from typing import List, Dict, Any, Callable

class DataProcessor:
    def __init__(self):
        self.operations = {}
        self.cache = {}
        self.lock = asyncio.Lock()

    def register_operation(self, name: str, operation: Callable[[List[Any]], Dict[str, Any]]):
        """指定した操作を登録する関数"""
        if name in self.operations:
            raise ValueError(f"操作名 '{name}' はすでに登録されています。")
        self.operations[name] = operation

    async def process_data(self, data: List[Any], operation_name: str) -> Dict[str, Any]:
        """データを非同期に処理し、指定した操作名に基づいて結果を返す関数"""
        async with self.lock:  # ロックを使用して競合状態を防ぐ
            if not data:
                return {'error': "データセットは空です。"}
            
            cache_key = f"{operation_name}:{tuple(data)}"
            if cache_key in self.cache:
                return self.cache[cache_key]

            if operation_name in self.operations:
                try:
                    result = await asyncio.to_thread(self.operations[operation_name], data)
                    self.cache[cache_key] = result  # 結果をキャッシュ
                    return result
                except Exception as e:
                    return {'error': f"処理中にエラーが発生しました: {str(e)}"}
            else:
                return {'error': f"無効な操作名 '{operation_name}' が指定されました。"}

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
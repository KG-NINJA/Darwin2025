import asyncio
from typing import List, Dict, Any, Optional, Union, Callable

class ExtendedDataProcessor:
    def __init__(self):
        self.operations = {}
        self.cache = {}
        self.lock = asyncio.Lock()  # 状態管理のためのロック

    def register_operation(self, name: str, operation: Callable[[List[Any]], Dict[str, Any]]):
        """指定した操作を登録する関数"""
        if name in self.operations:
            raise ValueError(f"操作名 '{name}' はすでに登録されています。")
        self.operations[name] = operation

    async def process_data(self, data: List[Any], operation_names: List[str]) -> List[Dict[str, Any]]:
        """データを非同期に処理し、指定した操作名に基づいて結果を返す関数"""
        async with self.lock:  # ロックを使用して競合状態を防ぐ
            results = []
            for operation_name in operation_names:
                if not data:
                    results.append({'error': "データが空です。"})
                    continue
                
                cache_key = f"{operation_name}:{tuple(data)}"
                if cache_key in self.cache:
                    results.append(self.cache[cache_key])
                    continue

                if operation_name in self.operations:
                    try:
                        result = await asyncio.to_thread(self.operations[operation_name], data)
                        self.cache[cache_key] = result  # 結果をキャッシュ
                        results.append(result)
                    except Exception as e:
                        results.append({'error': str(e)})
                else:
                    results.append({'error': f"無効な操作名 '{operation_name}' が指定されました。"})
            return results

async def calculate_statistics(data: List[Union[int, float]]) -> Dict[str, Any]:
    """データの統計情報（合計と平均）を計算する関数"""
    if not data:
        return {'error': "データが空です。"}
    stats = {'sum': sum(data), 'count': len(data), 'average': sum(data)/len(data)}
    return stats

# 使用例
data_processor = ExtendedDataProcessor()
data_processor.register_operation('statistics', calculate_statistics)

# 非同期にデータ処理
async def main():
    results = await data_processor.process_data([1, 2, 3, 4, 5], operation_names=['statistics'])
    print(results)

# asyncio.run(main())
from collections import defaultdict
from typing import List, Dict, Any, Optional, Union

class IntuitiveDataProcessor:
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Callable[[List[Union[int, float]]], Dict[str, Any]]):
        """指定した操作を登録する関数"""
        self.operations[name] = operation

    def process_data(self, data: List[Union[int, float]], operation_name: Optional[str] = None) -> Dict[str, Any]:
        """データを処理し、指定した操作名に基づいて結果を返す関数"""
        self._validate_data(data)
        if operation_name in self.operations:
            return self.operations[operation_name](data)
        raise ValueError(f"無効な操作名 '{operation_name}' が指定されました。")

    def _validate_data(self, data: List[Union[int, float]]):
        """データが正しい形式かを検証するプライベートメソッド"""
        if not data:
            raise ValueError("データが空です。")
        for num in data:
            if not isinstance(num, (int, float)):
                raise TypeError(f"無効なデータ型: {type(num)}. 整数または浮動小数点数が期待されます。")

def calculate_statistics(data: List[Union[int, float]]) -> Dict[str, Any]:
    """データの統計情報（合計と平均）を計算する関数"""
    stats = defaultdict(int)
    for num in data:
        stats['sum'] += num
        stats['count'] += 1
    stats['average'] = stats['sum'] / stats['count'] if stats['count'] > 0 else 0
    return stats

# 使用例
data_processor = IntuitiveDataProcessor()
data_processor.register_operation('statistics', calculate_statistics)
result = data_processor.process_data([1, 2, 3, 4, 5], operation_name='statistics')
print(result)
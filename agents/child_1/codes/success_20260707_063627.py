from collections import defaultdict
from typing import List, Dict, Any, Callable, Optional, Union

class StableDataProcessor:
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Callable[[List[Union[int, float]]], Dict[str, Any]]):
        self.operations[name] = operation

    def process_data(self, data: List[Union[int, float]], operation_name: Optional[str] = None) -> Dict[str, Any]:
        if not data:
            raise ValueError("Data is empty.")
        if operation_name and operation_name in self.operations:
            return self.operations[operation_name](data)
        raise ValueError(f"Invalid operation name '{operation_name}' supplied.")

def calculate_statistics(data: List[Union[int, float]]) -> Dict[str, Any]:
    """データの統計を計算し、平均を返す関数"""
    stats = defaultdict(int)
    for num in data:
        if isinstance(num, (int, float)):
            stats['sum'] += num
            stats['count'] += 1
        else:
            raise TypeError(f"Invalid data type: {type(num)}. Expected int or float.")
    stats['average'] = stats['sum'] / stats['count'] if stats['count'] > 0 else 0
    return stats

# 使用例
data_processor = StableDataProcessor()
data_processor.register_operation('statistics', calculate_statistics)
result = data_processor.process_data([1, 2, 3, 4, 5], operation_name='statistics')
print(result)
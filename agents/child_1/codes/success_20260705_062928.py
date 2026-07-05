from collections import defaultdict
from typing import List, Dict, Any, Callable

class DataProcessor:
    def __init__(self, operation: Callable[[List[int]], Dict[str, Any]]):
        self.operation = operation

    def process_data(self, data: List[int]) -> Dict[str, Any]:
        return self.operation(data)

def calculate_statistics(data: List[int]) -> Dict[str, Any]:
    # 統計を計算する関数
    stats = defaultdict(int)
    
    for num in data:
        stats['sum'] += num
        stats['count'] += 1
    
    # 平均計算
    if stats['count'] > 0:
        stats['average'] = stats['sum'] / stats['count']
    else:
        stats['average'] = 0

    return stats

# 使用例
data_processor = DataProcessor(calculate_statistics)
result = data_processor.process_data([1, 2, 3, 4, 5])
print(result)
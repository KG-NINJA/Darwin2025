from collections import defaultdict
from typing import List, Dict, Any, Callable, Optional

class FlexibleDataProcessor:
    def __init__(self):
        self.operations = {}

    def register_operation(self, name: str, operation: Callable[[List[int]], Dict[str, Any]]):
        self.operations[name] = operation

    def process_data(self, data: List[int], operation_name: Optional[str] = None) -> Dict[str, Any]:
        if operation_name and operation_name in self.operations:
            return self.operations[operation_name](data)
        raise ValueError("Invalid operation name supplied.")

def calculate_statistics(data: List[int]) -> Dict[str, Any]:
    stats = defaultdict(int)
    for num in data:
        stats['sum'] += num
        stats['count'] += 1
    if stats['count'] > 0:
        stats['average'] = stats['sum'] / stats['count']
    else:
        stats['average'] = 0
    return stats

# 使用例
data_processor = FlexibleDataProcessor()
data_processor.register_operation('statistics', calculate_statistics)
result = data_processor.process_data([1, 2, 3, 4, 5], operation_name='statistics')
print(result)
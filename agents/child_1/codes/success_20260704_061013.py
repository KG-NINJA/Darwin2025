from collections import defaultdict
from typing import List, Dict

def process_data(data: List[int]) -> Dict[str, int]:
    # データを一元管理
    stats = defaultdict(int)
    
    # リスト内包表記を使用して効率的に計算
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
data = [1, 2, 3, 4, 5]
result = process_data(data)
print(result)
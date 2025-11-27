from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Dict, Optional, Tuple, Callable

class Operation:
    """操作を表す基本クラス。各サブクラスでapplyメソッドを実装してください。"""
    def apply(self, item: Any) -> Any:
        raise NotImplementedError("必ず派生クラスで実装してください。")

class Double(Operation):
    """値を2倍にする操作"""
    def apply(self, item: float) -> float:
        return item * 2

class Increment(Operation):
    """値を1増やす操作"""
    def apply(self, item: float) -> float:
        return item + 1

class OperationManager:
    """複数の操作を管理するクラス"""
    def __init__(self, max_workers: Optional[int] = None):
        self.operations: Dict[str, Tuple[Callable[[Any], Any], str]] = {}
        self.max_workers = max_workers or 4  # デフォルトは4スレッド

    def register_operation(self, name: str, operation: Operation):
        """操作を登録"""
        self.operations[name] = (operation.apply, operation.__doc__)

    def run_operations(self, data: List[float]) -> Tuple[List[float], List[str]]:
        """登録された全ての操作をデータに適用し、結果とエラーメッセージを返す。"""
        results = []
        errors = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_operation = {
                executor.submit(op_func, item): (item, name, desc)
                for name, (op_func, desc) in self.operations.items()
                for item in data
            }

            for future in as_completed(future_to_operation):
                item, operation_name, operation_desc = future_to_operation[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    error_message = f"操作 '{operation_name}' ('{operation_desc}') でエラー: {str(e)}"
                    errors.append(error_message)
                    results.append(None)

        self.visualize_results(results)  # 追加: 実行結果の可視化
        return results, errors

    def visualize_results(self, results: List[Optional[float]]):
        """結果を可視化するメソッド"""
        print("操作結果:")
        for result in results:
            print(f"結果: {result}")
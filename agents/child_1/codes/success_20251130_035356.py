from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Dict, Optional, Tuple, Callable

class Operation:
    def apply(self, item: Any) -> Any:
        raise NotImplementedError("必ず派生クラスで実装してください。")

class Double(Operation):
    def apply(self, item: float) -> float:
        return item * 2

class Increment(Operation):
    def apply(self, item: float) -> float:
        return item + 1

class OperationManager:
    def __init__(self, max_workers: Optional[int] = None):
        self.operations: Dict[str, Tuple[Callable[[Any], Any], str]] = {}
        self.max_workers = max_workers or 4
        self.error_count = 0
        self.error_messages: List[str] = []

    def register_operation(self, name: str, operation: Operation):
        self.operations[name] = (operation.apply, operation.__doc__)

    def run_operations(self, data: List[float]) -> Tuple[List[Optional[float]], Dict[str, Any]]:
        results = []
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data_count = len(data) - len(valid_data)

        if invalid_data_count > 0:
            self.error_count += invalid_data_count
            self.error_messages.append(f"無効なデータ: {invalid_data_count} 件")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_operation = {
                executor.submit(op_func, item): (item, name, desc)
                for name, (op_func, desc) in self.operations.items()
                for item in valid_data
            }

            for future in as_completed(future_to_operation):
                item, operation_name, operation_desc = future_to_operation[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    error_message = f"操作 '{operation_name}' でエラー: {str(e)}"
                    self.error_messages.append(error_message)
                    self.error_count += 1
                    results.append(None)

        self.visualize_results(results)
        return results, {
            "error_count": self.error_count,
            "errors": self.error_messages,
        }

    def visualize_results(self, results: List[Optional[float]]):
        print("操作結果:")
        for result in results:
            print(f"結果: {result}")
        if self.error_messages:
            print("エラー一覧:")
            for message in self.error_messages:
                print(message)
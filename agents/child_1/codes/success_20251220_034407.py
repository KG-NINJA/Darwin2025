from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Any, Dict, Optional

class Operation:
    def __init__(self, func: Callable[[float], float], name: str):
        self.func = func
        self.name = name

    def apply(self, item: float) -> float:
        return self.func(item)

class OperationResult:
    def __init__(self, success: Optional[float] = None, error: Optional[str] = None):
        self.success = success
        self.error = error

class OperationManager:
    def __init__(self):
        self.operations: Dict[str, Operation] = {}
    
    def register_operation(self, func: Callable[[float], float], name: str):
        self.operations[name] = Operation(func, name)

    def run_operations(self, data: List[Any]) -> List[OperationResult]:
        results = []
        valid_data, invalid_data = self.validate_data(data)

        # スレッド数をデータのサイズに基づいて動的に調整
        max_workers = min(5, len(valid_data))  # 最大スレッド数は5、または有効データ数に基づく
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(op.apply, item): (item, op.name)
                for op in self.operations.values()
                for item in valid_data
            }

            for future in as_completed(futures):
                item, operation_name = futures[future]
                results.append(self.handle_future_result(future, operation_name, item))

        self.visualize_results(results, invalid_data)
        return results

    def handle_future_result(self, future, operation_name: str, item: Any) -> OperationResult:
        try:
            result = future.result()
            return OperationResult(success=result)
        except Exception as e:
            error_message = f"操作 '{operation_name}' でエラー: {str(e)} (データ: {item})"
            return OperationResult(error=error_message)

    def validate_data(self, data: List[Any]) -> (List[float], List[Any]):
        valid = [item for item in data if isinstance(item, (int, float))]
        invalid = [item for item in data if not isinstance(item, (int, float))]
        return valid, invalid

    def visualize_results(self, results: List[OperationResult], invalid_data: List[Any]):
        with open('results_log.txt', 'w') as log_file:  # ログファイルに書き込む
            for result in results:
                if result.success is not None:
                    log_file.write(f"成功: {result.success}\n")
                if result.error:
                    log_file.write(f"エラー: {result.error}\n")

            if invalid_data:
                log_file.write("スキップされた無効なデータ:\n")
                for item in invalid_data:
                    log_file.write(f"無効なデータ: {item}\n")

# 使用例
operation_manager = OperationManager()
operation_manager.register_operation(lambda x: x + 1, "Increment")
operation_manager.register_operation(lambda x: x ** 3, "Cube")
operation_manager.register_operation(lambda x: x ** 2, "Square")

data = [1, 2, 3, 'invalid', 4, 5]
results = operation_manager.run_operations(data)
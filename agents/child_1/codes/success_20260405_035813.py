from typing import Any, Callable, Dict, List, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

class Result:
    def __init__(self):
        self.successes: List[Tuple[Any, Any]] = []
        self.errors: List[Tuple[Any, str]] = []

    def add_success(self, item: Any, result: Any) -> None:
        self.successes.append((item, result))

    def add_error(self, item: Any, error_msg: str) -> None:
        self.errors.append((item, error_msg))

    def to_dict(self) -> Dict[str, List[Tuple]]:
        return {
            'successes': self.successes,
            'errors': self.errors
        }

class EnhancedOperationManager:
    """動的な操作を管理するクラス"""

    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """操作を登録する"""
        self.operations[name] = operation

    def run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = None) -> Dict[str, Any]:
        results = Result()
        max_workers = self._initialize_worker_count(max_workers, data)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_with_retries, item, op_name): item 
                       for item in data 
                       for op_name in chosen_operations
                       if op_name in self.operations}

            for future in as_completed(futures):
                item = futures[future]
                self._handle_future_result(future, item, results)

        return results.to_dict()

    def _initialize_worker_count(self, max_workers: int, data: List[Any]) -> int:
        return max_workers or len(data)

    def _execute_with_retries(self, item: Any, operation_name: str) -> Tuple[bool, Any, str]:
        for attempt in range(3):  # 再試行回数
            success, result, error_msg = self._run_single_operation(item, operation_name)
            if success:
                return (True, item, result)  # 成功
            if attempt == 2:  # 最終的なエラー返却
                return (False, item, error_msg)

    def _run_single_operation(self, item: Any, operation_name: str) -> Tuple[bool, Any, str]:
        operation = self.operations[operation_name]
        try:
            result = operation(item)
            return (True, result, None)  # 成功
        except Exception as e:
            error_msg = f"操作 '{operation_name}' においてエラー発生: {str(e)}"
            return (False, None, error_msg)  # エラー

    def _handle_future_result(self, future, item: Any, results: Result):
        try:
            success, item, result = future.result()
            if success:
                results.add_success(item, result)
            else:
                results.add_error(item, result)
        except Exception as e:
            results.add_error(item, f"未指定のエラー: {str(e)}")

# 使用例
if __name__ == "__main__":
    manager = EnhancedOperationManager()
    manager.register_operation("double", lambda x: x * 2)
    manager.register_operation("uppercase", lambda x: x.upper())
    result = manager.run_operations(["hello", 1, 2, 3, None], ["double", "uppercase"], max_workers=3)
    print(result)
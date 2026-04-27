import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any, Callable, Dict, List

class FlexibleOperationManager:
    def __init__(self):
        # 操作を管理する辞書
        self.operations: Dict[str, Callable[[Any], Any]] = {}
        # スレッドセーフな実行結果を保存するリスト
        self.results: List[Dict[str, Any]] = []
        self.lock = Lock()

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """新しい操作を登録します。"""
        if name in self.operations:
            logging.warning(f"Operation '{name}' is already registered. Overwriting.")
        self.operations[name] = operation

    def dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
        """選択した操作をデータに対して実行します。"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_operation, item, op_name): (item, op_name) 
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item, op_name = futures[future]
                result = future.result()
                with self.lock:
                    # 結果をリストに追加
                    self.results.append(result)

    def _execute_operation(self, item: Any, operation_name: str) -> Dict[str, Any]:
        """単一の操作を実行します。"""
        operation = self.operations.get(operation_name)
        if operation is None:
            error_msg = f"Operation '{operation_name}' not found for item '{item}'."
            logging.error(error_msg)
            return {'item': item, 'operation': operation_name, 'error': error_msg, 'success': False}
        try:
            result = operation(item)
            return {'item': item, 'operation': operation_name, 'result': result, 'success': True}
        except Exception as e:
            logging.error(f"Operation '{operation_name}' failed for item '{item}': {str(e)}")
            return {'item': item, 'operation': operation_name, 'error': f"Error: {str(e)} - Item: {item}", 'success': False}

    def get_results(self) -> List[Dict[str, Any]]:
        """保存された結果を取得します。"""
        with self.lock:
            return self.results
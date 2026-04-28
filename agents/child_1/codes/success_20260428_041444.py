import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any, Callable, Dict, List

class FlexibleOperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
        self.results: List[Dict[str, Any]] = []
        self.lock = Lock()

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """新しい操作を登録します。"""
        if name in self.operations:
            logging.warning(f"Operation '{name}' already registered. Overwriting.")
        self.operations[name] = operation
        self._visualize_operations()

    def _visualize_operations(self) -> None:
        """現在登録されている操作を視覚化します。"""
        logging.info(f"現在の登録操作: {list(self.operations.keys())}")

    def suggest_operations(self, input_name: str) -> List[str]:
        """類似の操作名の提案を返します。"""
        return [name for name in self.operations if input_name in name]

    def dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
        """選択した操作をデータに対して実行します。"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_operation, item, op_name): (item, op_name) 
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item, op_name = futures[future]
                result = future.result()
                with self.lock:
                    self.results.append(result)

    def _execute_operation(self, item: Any, operation_name: str) -> Dict[str, Any]:
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
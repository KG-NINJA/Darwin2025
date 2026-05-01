import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any, Callable, Dict, List, Tuple

class FlexibleOperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
        self.results: List[Dict[str, Any]] = []
        self.lock = Lock()
        self.current_progress: Dict[str, int] = {}

    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """新しい操作を登録します。"""
        if name in self.operations:
            logging.warning(f"Operation '{name}' is already registered. Overwriting.")
        self.operations[name] = operation
        self._visualize_operations()

    def _visualize_operations(self) -> None:
        """登録されている操作を視覚化します。"""
        logging.info(f"現在の登録操作: {list(self.operations.keys())}")

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
                    self._update_progress(op_name)

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
            error_msg = f"Operation '{operation_name}' failed for item '{item}': {str(e)}"
            logging.error(error_msg)
            return {'item': item, 'operation': operation_name, 'error': f"Error: {str(e)} - Item: {item}", 'success': False}

    def _update_progress(self, operation_name: str) -> None:
        """操作の進捗を更新します。"""
        if operation_name not in self.current_progress:
            self.current_progress[operation_name] = 0
        self.current_progress[operation_name] += 1
        logging.info(f"進捗更新: {operation_name} - 完了数: {self.current_progress[operation_name]}")

    def visualize_progress(self) -> None:
        """進捗を可視化する機能を追加します。"""
        total_operations = sum(self.current_progress.values())
        logging.info(f"全操作の進捗: {total_operations} / {len(self.operations)}")

    def graph_analysis(self):
        """進捗状況をグラフで視覚化し、ユーザーにフィードバックを提供します。"""
        # グラフィカルな出力処理をここに追加
        pass
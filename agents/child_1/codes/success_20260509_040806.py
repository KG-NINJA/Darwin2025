from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any, Dict, Callable
import logging
import threading

class OperationManager:
    def __init__(self):
        self.results = []
        self.lock = threading.Lock()
        self.operations = {}
        self.dependency_map = {}
        self.status_cache = set()  # ここでキャッシュを追加

    def run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
        """選択した操作をデータに対して実行します。"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._execute_operation, item, op_name): (item, op_name)
                for item in data
                for op_name in chosen_operations 
                if self._check_dependencies(op_name)
            }

            for future in as_completed(futures):
                item, op_name = futures[future]
                self._handle_future_result(item, op_name, future)

        self._visualize_progress()

    def _handle_future_result(self, item: Any, op_name: str, future) -> None:
        """Futureの結果を処理し、進捗を更新します。"""
        try:
            result = future.result()
            self._handle_result(item, op_name, result)
        except Exception as e:
            self._log_error(op_name, item, str(e))

    def _handle_result(self, item: Any, op_name: str, result: Dict[str, Any]) -> None:
        """結果を処理し、進捗を更新します。"""
        if result.get('success', False):
            with self.lock:
                self.results.append(result)
                self.status_cache.add(op_name)  # 完了オペレーションをキャッシュ
                self._update_progress(op_name)
        else:
            self._log_error(op_name, item, result.get('error'))

    def _log_error(self, op_name: str, item: Any, error: str) -> None:
        logging.error(f"エラー発生: '{error}' - '{op_name}' に対して '{item}'")

    def _visualize_progress(self) -> None:
        """進捗を視覚的に表示します。"""
        total_operations = len(self.results)
        total_operations_count = len(self.operations)
        percentage_complete = (total_operations / total_operations_count * 100) if total_operations_count else 0
        logging.info(f"進捗状況: {total_operations} / {total_operations_count} - 完了率: {percentage_complete:.2f}%")

    def _check_dependencies(self, op_name: str) -> bool:
        """依存関係をチェックします。キャッシュを使用して効率を向上させます。"""
        if op_name in self.status_cache:  # キャッシュを確認
            return True

        dependencies = self.dependency_map.get(op_name, [])
        return all(dep in self.results for dep in dependencies)

    def add_operation(self, op_name: str, func: Callable, dependencies: List[str] = None) -> None:
        """新しいオペレーションを追加します。"""
        self.operations[op_name] = func
        if dependencies is None:
            dependencies = []
        self.dependency_map[op_name] = dependencies
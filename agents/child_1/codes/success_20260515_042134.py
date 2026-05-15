from typing import Any, Callable, Dict, List
import logging
import threading

class OperationManager:
    def __init__(self):
        self.operations = {}
        self.results = []
        self.status_cache = set()
        self.lock = threading.Lock()

    def add_operation(self, op_name: str, func: Callable, dependencies: List[str] = None) -> None:
        """新しいオペレーションを追加し、依存関係を設定します。"""
        self.operations[op_name] = {
            "func": func,
            "dependencies": dependencies or []
        }

    def run_operations(self):
        """全オペレーションを並行で実行します。"""
        threads = []
        for op_name, op in self.operations.items():
            if self._check_dependencies(op_name):
                thread = threading.Thread(target=self._execute_operation, args=(op_name,))
                threads.append(thread)
                thread.start()
        
        for thread in threads:
            thread.join()  # 全てのスレッドが終了するのを待つ

    def _execute_operation(self, op_name: str):
        """指定された操作を実行し、その結果を返します。"""
        operation = self.operations.get(op_name)
        if operation:
            try:
                result = operation["func"]()
                self._update_success(op_name, result)
            except Exception as e:
                self._log_error(op_name, str(e))

    def _update_success(self, op_name: str, result: Any) -> None:
        """成功した結果をキャッシュし、進捗を更新します。"""
        with self.lock:
            self.results.append(result)
            self.status_cache.add(op_name)
            self._visualize_progress()

    def _log_error(self, op_name: str, error: str) -> None:
        logging.error(f"エラー: '{error}' - 操作: '{op_name}'")
        
    def _visualize_progress(self) -> None:
        """進捗を視覚的に表示します。"""
        total_operations = len(self.results)
        total_operations_count = len(self.operations)
        percentage_complete = (total_operations / total_operations_count * 100) if total_operations_count else 0
        logging.info(f"進捗状況: {total_operations} / {total_operations_count} - 完了率: {percentage_complete:.2f}%")

    def _check_dependencies(self, op_name: str) -> bool:
        """依存関係をチェックします。"""
        return all(dep in self.status_cache for dep in self.operations[op_name]["dependencies"])
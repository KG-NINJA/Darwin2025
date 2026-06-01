import logging
import threading
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

class EnhancedOperationManager:
    def __init__(self, thread_limit: int = 5, retry_limit: int = 3):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: List[Dict[str, Any]] = []  
        self.error_messages: List[str] = []
        self.lock = threading.Lock()
        self.thread_limit = thread_limit
        self.retry_limit = retry_limit
        self.failed_operations: List[str] = []
        self.thread_pool: List[threading.Thread] = []

    def add_operation(self, op_name: str, func: Callable, dependencies: Optional[List[str]] = None) -> None:
        """オペレーションを追加します。"""
        if op_name not in self.operations:
            self.operations[op_name] = {
                "func": func,
                "dependencies": dependencies or [],
                "is_completed": False,
                "retry_attempts": 0,
            }
        else:
            logging.warning(f"Operation '{op_name}' already exists.")

    def run_operations(self):
        """オペレーションを実行します。"""
        while self.operations:
            active_threads = len(self.thread_pool)
            for op_name in list(self.operations.keys()):
                if self._are_dependencies_met(op_name) and active_threads < self.thread_limit:
                    thread = threading.Thread(target=self._execute_with_retry, args=(op_name,))
                    thread.start()
                    self.thread_pool.append(thread)
                    active_threads += 1

            self._cleanup_operations()
            self._wait_for_threads()

    def _wait_for_threads(self) -> None:
        """スレッドが完了するのを待ちます。"""
        for thread in self.thread_pool:
            thread.join()
        self.thread_pool = [thread for thread in self.thread_pool if thread.is_alive()]

    def _execute_with_retry(self, op_name: str):
        """リトライ機能を付加してオペレーションを実行します。"""
        operation = self.operations[op_name]
        while operation['retry_attempts'] < self.retry_limit:
            try:
                result = operation["func"]()
                self._record_success(op_name, result)
                break
            except Exception as e:
                self._log_error(op_name, str(e))
                operation['retry_attempts'] += 1
                if operation['retry_attempts'] >= self.retry_limit:
                    self.failed_operations.append(op_name)
                    logging.error(f"Failed '{op_name}' after {self.retry_limit} attempts.")

    def _record_success(self, op_name: str, result: Any) -> None:
        """成功したオペレーションを記録します。"""
        timestamp = datetime.now().isoformat()
        with self.lock:
            self.results.append({"op_name": op_name, "result": result, "timestamp": timestamp})
            self.operations[op_name]['is_completed'] = True
            logging.info(f"Operation '{op_name}' completed successfully at {timestamp}.")

    def _log_error(self, op_name: str, error: str) -> None:
        """エラーメッセージを記録します。"""
        with self.lock:
            logging.error(f"Error in '{op_name}': {error}")
            self.error_messages.append(f"Operation: '{op_name}', Error: '{error}'")

    def _are_dependencies_met(self, op_name: str) -> bool:
        """依存関係が満たされているかを評価します。"""
        return all(dep in [result["op_name"] for result in self.results] for dep in self.operations[op_name]["dependencies"])

    def _cleanup_operations(self) -> None:
        """冗長な操作情報をクリアします。"""
        with self.lock:
            self.operations = {k: v for k, v in self.operations.items() if not v['is_completed']}
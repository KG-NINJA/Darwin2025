from threading import Thread, Lock
from time import sleep
from datetime import datetime
import logging
from typing import Callable, List, Any, Optional, Dict

class OperationManager:
    def __init__(self, thread_limit: int, retry_limit: int, retry_interval: int):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()
        self.thread_limit = thread_limit
        self.retry_limit = retry_limit
        self.retry_interval = retry_interval
        self.failed_operations: List[str] = []
        self.thread_pool: List[Thread] = []

    def add_operation(self, op_name: str, func: Callable[..., Any], dependencies: Optional[List[str]] = None) -> None:
        """オペレーションを追加します。"""
        if op_name in self.operations:
            logging.warning(f"Operation '{op_name}' already exists.")
            return
        self.operations[op_name] = {
            "func": func,
            "dependencies": dependencies or [],
            "is_completed": False,
            "retry_attempts": 0,
        }

    def run_operations(self) -> None:
        """オペレーションを実行します。"""
        while self.operations:
            self._execute_ready_operations()
            self._cleanup_operations()
            self._join_completed_threads()

    def _execute_ready_operations(self) -> None:
        """依存関係が満たされているオペレーションを実行します。"""
        for op_name in list(self.operations.keys()):
            if self._are_dependencies_met(op_name) and len(self.thread_pool) < self.thread_limit:
                thread = Thread(target=self._execute_with_retry, args=(op_name,))
                thread.start()
                self.thread_pool.append(thread)

    def _execute_with_retry(self, op_name: str) -> None:
        """リトライ機能を付加してオペレーションを実行します。"""
        operation = self.operations[op_name]
        while operation['retry_attempts'] < self.retry_limit:
            try:
                result = operation['func']()
                self._record_success(op_name, result)
                return
            except Exception as e:
                self._handle_error(op_name, str(e))
                sleep(self.retry_interval)
                operation['retry_attempts'] += 1
                logging.info(f"{op_name}のエラーが発生しました。リトライ中...")

        self.failed_operations.append(op_name)
        logging.error(f"Operation '{op_name}' failed after {self.retry_limit} attempts.")

    def _record_success(self, op_name: str, result: Any) -> None:
        """成功したオペレーションを記録します。"""
        with self.lock:
            timestamp = datetime.now().isoformat()
            self.results[op_name] = {"result": result, "timestamp": timestamp}
            self.operations[op_name]['is_completed'] = True
            logging.info(f"Operation '{op_name}' completed successfully at {timestamp}.")

    def _handle_error(self, op_name: str, error: str) -> None:
        """エラーメッセージを記録し、ロギングします。"""
        with self.lock:
            timestamp = datetime.now().isoformat()
            error_message = (f"Operation: '{op_name}', "
                             f"Attempt: {self.operations[op_name]['retry_attempts'] + 1}, "
                             f"Error: '{error}' at {timestamp}")
            logging.error(error_message)

    def _are_dependencies_met(self, op_name: str) -> bool:
        """依存関係が満たされているかを評価します。"""
        return all(dep in self.results for dep in self.operations[op_name]["dependencies"])

    def _cleanup_operations(self) -> None:
        """冗長な操作情報をクリアします。"""
        with self.lock:
            self.operations = {k: v for k, v in self.operations.items() if not v['is_completed']}

    def _join_completed_threads(self) -> None:
        """完了したスレッドを結合します。"""
        for thread in list(self.thread_pool):
            if not thread.is_alive():
                thread.join()
                self.thread_pool.remove(thread)
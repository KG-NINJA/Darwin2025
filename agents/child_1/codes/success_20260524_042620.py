import logging
import threading
from typing import Any, Callable, Dict, List, Optional

class SimpleOperationManager:
    def __init__(self):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: List[Any] = []
        self.error_messages: List[str] = []
        self.lock = threading.Lock()
        self.thread_limit: int = 5  # 同時スレッド数
        self.retry_limit: int = 3  # 再試行回数

    def add_operation(self, op_name: str, func: Callable, dependencies: Optional[List[str]] = None) -> None:
        if op_name not in self.operations:
            self.operations[op_name] = {
                "func": func,
                "dependencies": dependencies or []
            }
        else:
            logging.warning(f"Operation '{op_name}' already exists.")

    def run_operations(self):
        while self.operations:
            threads = []
            for op_name in list(self.operations.keys()):
                if self._are_dependencies_met(op_name) and len(threads) < self.thread_limit:
                    thread = threading.Thread(target=self._execute_with_retry, args=(op_name,))
                    threads.append(thread)
                    thread.start()
                    del self.operations[op_name]
            
            for thread in threads:
                thread.join()

    def _execute_with_retry(self, op_name: str):
        operation = self.operations[op_name]
        for attempt in range(self.retry_limit):
            try:
                result = operation["func"]()
                self._record_success(op_name, result)
                break
            except Exception as e:
                self._log_error(op_name, str(e))
                if attempt + 1 >= self.retry_limit:
                    logging.error(f"Failed '{op_name}' after {self.retry_limit} attempts.")

    def _record_success(self, op_name: str, result: Any) -> None:
        with self.lock:
            self.results.append(result)
            logging.info(f"Operation '{op_name}' completed successfully.")

    def _log_error(self, op_name: str, error: str) -> None:
        with self.lock:
            logging.error(f"Error: '{error}' - Operation: '{op_name}'")
            self.error_messages.append(f"Operation: '{op_name}', Error: '{error}'")

    def _are_dependencies_met(self, op_name: str) -> bool:
        return all(dep in self.results for dep in self.operations[op_name]["dependencies"])
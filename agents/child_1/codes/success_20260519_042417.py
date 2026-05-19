from typing import Any, Callable, Dict, List, Optional
import logging
import threading

class EnhancedOperationManager:
    def __init__(self):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: List[Any] = []
        self.status_cache: set = set()
        self.lock: threading.Lock = threading.Lock()
        self.error_messages: List[str] = []
        self.retry_limit: int = 3
        self.thread_limit: int = 5  # 最大スレッド数の制限

    def add_operation(self, op_name: str, func: Callable, dependencies: Optional[List[str]] = None) -> None:
        if op_name not in self.operations:
            self.operations[op_name] = {
                "func": func,
                "dependencies": dependencies or []
            }
        else:
            logging.warning(f"Operation '{op_name}' already exists.")

    def run_operations(self):
        threads = []
        for op_name, op in self.operations.items():
            if self._check_dependencies(op_name) and len(threads) < self.thread_limit:
                thread = threading.Thread(target=self._execute_operation, args=(op_name,))
                threads.append(thread)
                thread.start()
        
        for thread in threads:
            thread.join()

    def _execute_operation(self, op_name: str):
        operation = self.operations.get(op_name)
        attempt = 0
        success = False
        
        while attempt < self.retry_limit and not success:
            try:
                result = operation["func"]()
                self._update_success(op_name, result)
                success = True
            except Exception as e:
                self._log_error(op_name, str(e))
                attempt += 1
                if attempt == self.retry_limit:
                    logging.error(f"Operation '{op_name}' failed after {self.retry_limit} retries.")

    def _update_success(self, op_name: str, result: Any) -> None:
        with self.lock:
            self.results.append(result)
            self.status_cache.add(op_name)
            self._visualize_progress()

    def _log_error(self, op_name: str, error: str) -> None:
        logging.error(f"Error: '{error}' - Operation: '{op_name}'")
        self.error_messages.append(f"Operation: '{op_name}', Error: '{error}'")

    def _visualize_progress(self) -> None:
        total_operations = len(self.results)
        total_operations_count = len(self.operations)
        percentage_complete = (total_operations / total_operations_count * 100) if total_operations_count else 0
        logging.info(f"Progress: {total_operations} / {total_operations_count} - Completion: {percentage_complete:.2f}%")

    def _check_dependencies(self, op_name: str) -> bool:
        return all(dep in self.status_cache for dep in self.operations[op_name]["dependencies"])
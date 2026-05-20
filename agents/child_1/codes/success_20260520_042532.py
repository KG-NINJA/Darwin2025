import logging
import threading
from typing import Any, Callable, Dict, List, Optional

class OptimizedOperationManager:
    def __init__(self):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: List[Any] = []
        self.error_messages: List[str] = []
        self.thread_limit: int = 5  # 同時スレッド数

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
            for op_name, op in list(self.operations.items()):
                if self._check_dependencies(op_name) and len(threads) < self.thread_limit:
                    thread = threading.Thread(target=self._execute_operation, args=(op_name,))
                    threads.append(thread)
                    thread.start()
                    del self.operations[op_name]  # オペレーションを削除
            
            for thread in threads:
                thread.join()

    def _execute_operation(self, op_name: str):
        operation = self.operations.get(op_name)
        try:
            result = operation["func"]()
            self._update_success(op_name, result)
        except ValueError as ve:
            self._handle_value_error(op_name, str(ve))
        except Exception as e:
            self._log_error(op_name, str(e))

    def _update_success(self, op_name: str, result: Any) -> None:
        self.results.append(result)
        logging.info(f"Operation '{op_name}' completed successfully.")

    def _log_error(self, op_name: str, error: str) -> None:
        logging.error(f"Error: '{error}' - Operation: '{op_name}'")
        self.error_messages.append(f"Operation: '{op_name}', Error: '{error}'")

    def _handle_value_error(self, op_name: str, error: str) -> None:
        logging.warning(f"ValueError detected in '{op_name}': {error}")
        # 特定のリカバリ処理をここで定義

    def _check_dependencies(self, op_name: str) -> bool:
        return all(dep in self.results for dep in self.operations[op_name]["dependencies"])
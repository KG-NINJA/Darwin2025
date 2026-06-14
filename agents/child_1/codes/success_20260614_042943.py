from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from datetime import datetime
from typing import Callable, List, Any, Optional

class OperationManager:
    def __init__(self, thread_limit: int, retry_limit: int, retry_interval: int) -> None:
        self.thread_limit = thread_limit
        self.retry_limit = retry_limit
        self.retry_interval = retry_interval
        self.failed_operations: List[str] = []
        self.results: dict = {}
        self.operations: dict = {}

    def add_operation(self, op_name: str, func: Callable[..., Any], dependencies: Optional[List[str]] = None) -> None:
        if op_name in self.operations:
            logging.warning(f"Operation '{op_name}' already exists.")
            return
        self.operations[op_name] = {
            "func": func,
            "dependencies": dependencies or [],
            "is_completed": False,
        }

    def run_operations(self) -> None:
        with ThreadPoolExecutor(max_workers=self.thread_limit) as executor:
            future_to_op = {executor.submit(self._execute_with_retry, op_name): op_name for op_name in self.operations}

            for future in as_completed(future_to_op):
                op_name = future_to_op[future]
                try:
                    future.result()
                except Exception:
                    self.failed_operations.append(op_name)
                    logging.error(f"Operation '{op_name}' failed.")

    def _execute_with_retry(self, op_name: str) -> None:
        operation = self.operations[op_name]
        for attempt in range(self.retry_limit):
            try:
                result = operation['func']()
                self._record_success(op_name, result)
                return
            except Exception as e:
                self._handle_error(op_name, str(e), attempt + 1)

        logging.error(f"Operation '{op_name}' failed after {self.retry_limit} attempts.")

    def _record_success(self, op_name: str, result: Any) -> None:
        timestamp = datetime.now().isoformat()
        self.results[op_name] = {"result": result, "timestamp": timestamp}
        self.operations[op_name]['is_completed'] = True
        logging.info(f"Operation '{op_name}' completed successfully at {timestamp}.")

    def _handle_error(self, op_name: str, error: str, attempt: int) -> None:
        timestamp = datetime.now().isoformat()
        error_message = (f"Operation: '{op_name}', "
                         f"Attempt: {attempt}, "
                         f"Error: '{error}' at {timestamp}")
        logging.error(error_message)

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Callable, Any, Dict, List


class OperationManager:
    def __init__(self, thread_limit: int = 4, retry_limit: int = 3):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
        self.failed_operations: Dict[str, int] = {}
        self.thread_limit = thread_limit
        self.retry_limit = retry_limit

    def add_operation(self, op_name: str, func: Callable, dependencies: List[str] = None) -> None:
        if op_name in self.operations:
            logging.warning(f"Operation '{op_name}' already exists.")
            return
        self.operations[op_name] = {
            "func": func,
            "dependencies": dependencies or [],
            "is_completed": False,
        }

        for dep in dependencies or []:
            self.dependency_graph.setdefault(dep, []).append(op_name)

    def run_operations(self) -> None:
        order_of_execution = self._get_execution_order()
        with ThreadPoolExecutor(max_workers=self.thread_limit) as executor:
            future_to_op = {
                executor.submit(self._execute_operation, op_name): op_name for op_name in order_of_execution
            }

            for future in as_completed(future_to_op):
                op_name = future_to_op[future]
                try:
                    future.result()
                except Exception as e:
                    self._handle_operation_failure(op_name, str(e))

    def _execute_operation(self, op_name: str) -> None:
        operation = self.operations[op_name]
        for attempt in range(self.retry_limit):
            try:
                result = operation['func']()
                self._record_success(op_name, result)
                return
            except Exception as e:
                self._handle_error(op_name, str(e), attempt + 1)
                if attempt + 1 < self.retry_limit:
                    logging.info(f"Retrying operation '{op_name}'...")

        self.failed_operations[op_name] = self.retry_limit
        logging.error(f"Operation '{op_name}' failed after {self.retry_limit} attempts.")
        self._skip_dependent_operations(op_name)

    def _handle_operation_failure(self, op_name: str, error: str) -> None:
        logging.error(f"Operation '{op_name}' failed: {error}")
        self._log_failure_details(op_name)

    # ... (残りのメソッドは変更なしですが、エラーハンドリングの改善を含む)
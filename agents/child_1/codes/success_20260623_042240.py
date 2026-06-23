import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Callable, Any, Dict, List


class EnhancedOperationManager:
    def __init__(self, thread_limit: int = 4, retry_limit: int = 3):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Any] = {}
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
        self._validate_dependencies(dependencies)
        
    def _validate_dependencies(self, dependencies: List[str]) -> None:
        for dep in dependencies or []:
            if dep not in self.operations:
                logging.error(f"Dependency '{dep}' for operation '{op_name}' does not exist.")
            else:
                logging.info(f"Dependency '{dep}' is valid for operation '{op_name}'.")

    def run_operations(self) -> None:
        ordered_operations = self._get_execution_order()
        with ThreadPoolExecutor(max_workers=self.thread_limit) as executor:
            future_to_op = {executor.submit(self._execute_operation, op_name): op_name for op_name in ordered_operations}

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
                self.results[op_name] = result
                operation['is_completed'] = True
                return
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1} failed for '{op_name}': {e}")
                if attempt + 1 == self.retry_limit:
                    self.failed_operations[op_name] = self.retry_limit
                    logging.error(f"Operation '{op_name}' failed after {self.retry_limit} attempts.")

    def _handle_operation_failure(self, op_name: str, error: str) -> None:
        logging.error(f"Operation '{op_name}' failed: {error}")

    def _get_execution_order(self) -> List[str]:
        return sorted(self.operations.keys(), key=lambda x: len(self.operations[x]['dependencies']))

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any, Dict, List, Union

class DynamicOperationManager:
    def __init__(self, thread_limit: int = 4):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Union[Any, Dict[str, Any]]] = {}
        self.failed_operations: Dict[str, int] = {}
        self.thread_limit = thread_limit

    def add_operation(self, op_name: str, func: Callable, dependencies: List[str] = None, result_format: str = None) -> None:
        if op_name in self.operations:
            logging.warning(f"Operation '{op_name}' already exists.")
            return
            
        self.operations[op_name] = {
            "func": func,
            "dependencies": dependencies or [],
            "is_completed": False,
            "result_format": result_format,
        }
        self._validate_dependencies(dependencies)

    def _validate_dependencies(self, dependencies: List[str]) -> None:
        for dep in dependencies or []:
            if dep not in self.operations:
                logging.error(f"Dependency '{dep}' for operation '{dep}' does not exist.")

    def run_operations(self) -> None:
        ordered_operations = self._get_execution_order()
        with ThreadPoolExecutor(max_workers=self.thread_limit) as executor:
            future_to_op = {executor.submit(self._execute_operation, op_name): op_name for op_name in ordered_operations}

            for future in as_completed(future_to_op):
                op_name = future_to_op[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Operation '{op_name}' failed with error: {e}")

    def _execute_operation(self, op_name: str) -> None:
        operation = self.operations[op_name]
        try:
            result = operation['func']()
            if operation.get('result_format'):
                result = self._format_result(result, operation['result_format'])
            self.results[op_name] = result
            operation['is_completed'] = True
        except Exception as e:
            self.failed_operations[op_name] = 1
            logging.error(f"Operation '{op_name}' failed: {e}")

    def _get_execution_order(self) -> List[str]:
        return sorted(self.operations.keys(), key=lambda x: len(self.operations[x]['dependencies']))

    def _format_result(self, result: Any, format_type: str) -> Any:
        if format_type == "json":
            import json
            return json.dumps(result)
        return result  # Default fallback
import logging
import asyncio
from typing import Callable, Any, Dict, List, Union

class AsyncOperationManager:
    def __init__(self):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Union[Any, Dict[str, Any]]] = {}
        self.failed_operations: Dict[str, int] = {}

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
                logging.error(f"Dependency '{dep}' for operation '{dep}' does not exist.")

    async def run_operations(self) -> None:
        ordered_operations = self._get_execution_order()
        tasks = [self._execute_operation(op_name) for op_name in ordered_operations]
        await asyncio.gather(*tasks)

    async def _execute_operation(self, op_name: str) -> None:
        operation = self.operations[op_name]
        try:
            result = await operation['func']()
            self.results[op_name] = result
            operation['is_completed'] = True
        except Exception as e:
            self.failed_operations[op_name] = 1
            logging.error(f"Operation '{op_name}' failed: {e}")

    def _get_execution_order(self) -> List[str]:
        return sorted(self.operations.keys(), key=lambda x: len(self.operations[x]['dependencies']))

# Example usage:
async def sample_operation():
    await asyncio.sleep(1)
    return "Operation Complete"
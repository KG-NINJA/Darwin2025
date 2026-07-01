import logging
import asyncio
from typing import Callable, Any, Dict, List

class EnhancedAsyncOperationManager:
    def __init__(self, timeout: int = 5):
        self.operations: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Any] = {}
        self.failed_operations: List[str] = []
        self.timeout = timeout

    def add_operation(self, op_name: str, func: Callable, metadata: Dict[str, Any] = None, dependencies: List[str] = None) -> None:
        if op_name in self.operations:
            logging.warning(f"Operation '{op_name}' already exists.")
            return
        self.operations[op_name] = {
            "func": func,
            "metadata": metadata or {},
            "dependencies": dependencies or [],
            "is_completed": False,
        }
        if dependencies:
            self._validate_dependencies(op_name, dependencies)

    def _validate_dependencies(self, op_name: str, dependencies: List[str]) -> None:
        for dep in dependencies:
            if dep not in self.operations:
                logging.error(f"Operation '{op_name}' has a missing dependency: '{dep}'.")
                raise ValueError(f"Missing dependency: '{dep}' for operation '{op_name}'.")

    async def run_operations(self) -> None:
        ordered_operations = self._get_execution_order()
        tasks = [self._execute_operation(op_name) for op_name in ordered_operations]
        await asyncio.gather(*tasks)

    async def _execute_operation(self, op_name: str) -> None:
        operation = self.operations[op_name]
        try:
            result = await asyncio.wait_for(operation['func'](), timeout=self.timeout)
            self.results[op_name] = result
            operation['is_completed'] = True
            logging.info(f"Operation '{op_name}' completed successfully.")
        except asyncio.TimeoutError:
            self.failed_operations.append(op_name)
            logging.error(f"Operation '{op_name}' timed out after {self.timeout} seconds.")
        except Exception as e:
            self.failed_operations.append(op_name)
            logging.error(f"Operation '{op_name}' failed: {e}")

    def _get_execution_order(self) -> List[str]:
        return sorted(self.operations.keys(), key=lambda x: len(self.operations[x]['dependencies']))

    def visualize_operations(self) -> None:
        for op_name, operation in self.operations.items():
            status = "Completed" if operation['is_completed'] else "Pending"
            logging.info(f"Operation: {op_name}, Status: {status}, Metadata: {operation['metadata']}")

# Example usage
async def sample_operation():
    await asyncio.sleep(2)  # Simulate work
    return "Operation successful"
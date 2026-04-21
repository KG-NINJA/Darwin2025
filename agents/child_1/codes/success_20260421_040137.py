import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List

class FlexibleOperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
    
    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """新しい操作を登録します。"""
        self.operations[name] = operation

    def dynamic_run_operations(self, data: List[Any], chosen_operations: List[str]) -> List[Dict[str, Any]]:
        """選択した操作をデータに対して実行し、結果を返します。"""
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._execute_operation, item, op_name): (item, op_name) 
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item, op_name = futures[future]
                results.append(future.result())

        return results
    
    def _execute_operation(self, item: Any, operation_name: str) -> Dict[str, Any]:
        """単一の操作を実行します。"""
        operation = self.operations[operation_name]
        try:
            result = operation(item)
            return {'item': item, 'operation': operation_name, 'result': result, 'success': True}
        except Exception as e:
            logging.error(f"Operation '{operation_name}' failed for item '{item}': {str(e)}")
            return {'item': item, 'operation': operation_name, 'error': str(e), 'success': False}
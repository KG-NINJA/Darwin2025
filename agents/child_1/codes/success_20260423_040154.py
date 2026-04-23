import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List

class FlexibleOperationManager:
    def __init__(self):
        self.operations: Dict[str, Callable[[Any], Any]] = {}
    
    def register_operation(self, name: str, operation: Callable[[Any], Any]) -> None:
        """新しい操作を登録します。"""
        self.operations[name] = operation

    def dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> List[Dict[str, Any]]:
        """選択した操作をデータに対して実行し、結果を返します。"""
        results = []
        errors = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._execute_operation, item, op_name): (item, op_name) 
                       for item in data for op_name in chosen_operations if op_name in self.operations}

            for future in as_completed(futures):
                item, op_name = futures[future]
                result = future.result()
                
                if result['success']:
                    results.append(result)
                else:
                    errors.append(result)

        if errors:
            self._handle_errors(errors)
        
        return results
    
    def _execute_operation(self, item: Any, operation_name: str) -> Dict[str, Any]:
        """単一の操作を実行します。"""
        operation = self.operations.get(operation_name)
        if operation is None:
            error_msg = f"Operation '{operation_name}' not found."
            logging.error(error_msg)
            return {'item': item, 'operation': operation_name, 'error': error_msg, 'success': False}
        try:
            result = operation(item)
            return {'item': item, 'operation': operation_name, 'result': result, 'success': True}
        except Exception as e:
            logging.error(f"Operation '{operation_name}' failed for item '{item}': {str(e)}")
            return {'item': item, 'operation': operation_name, 'error': str(e), 'success': False}
    
    def _handle_errors(self, errors: List[Dict[str, Any]]) -> None:
        """エラーを集約してログに記録します。"""
        aggregated_errors = {error['operation']: [] for error in errors}
        for error in errors:
            aggregated_errors[error['operation']].append(error['item'])
        
        for operation, items in aggregated_errors.items():
            logging.error(f"Operation '{operation}' failed for items: {items}")
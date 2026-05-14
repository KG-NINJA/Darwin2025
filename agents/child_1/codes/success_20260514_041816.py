from typing import Any, Callable, Dict, List
import logging

class OperationManager:
    def __init__(self):
        self.operations = {}
        self.results = []
        self.status_cache = set()
        self.dependency_map = {}
        self.lock = None  # Assuming a threading.Lock()

    def add_operation(self, op_name: str, func: Callable, dependencies: List[str] = None) -> None:
        """新しいオペレーションを追加し、依存関係を設定します。"""
        self.operations[op_name] = func
        self.dependency_map[op_name] = dependencies or []

    def run_operations(self):
        """全オペレーションを実行します。"""
        for op_name in self.operations.keys():
            if self._check_dependencies(op_name):
                result = self._execute_operation(op_name)
                if result.get('success', False):
                    self._update_success(op_name, result)
                else:
                    self._log_error(op_name, result.get('error'))

    def _execute_operation(self, op_name: str) -> Dict[str, Any]:
        """指定された操作を実行し、その結果を返します。"""
        operation = self.operations.get(op_name)
        if operation:
            try:
                result = operation()
                return {'success': True, 'data': result}
            except Exception as e:
                return {'success': False, 'error': f'操作 {op_name} の実行中にエラーが発生: {str(e)}'}
        return {'success': False, 'error': f'操作 {op_name} が見つかりません。'}

    def _update_success(self, op_name: str, result: Dict[str, Any]) -> None:
        """成功した結果をキャッシュし、進捗を更新します。"""
        with self.lock:
            self.results.append(result)
            self.status_cache.add(op_name)
            self._update_progress(op_name)

    def _log_error(self, op_name: str, error: str) -> None:
        logging.error(f"エラー発生: '{error}' - 操作: '{op_name}'")
        
    def _visualize_progress(self) -> None:
        """進捗を視覚的に表示します。"""
        total_operations = len(self.results)
        total_operations_count = len(self.operations)
        percentage_complete = (total_operations / total_operations_count * 100) if total_operations_count else 0
        logging.info(f"進捗状況: {total_operations} / {total_operations_count} - 完了率: {percentage_complete:.2f}%")

    def _check_dependencies(self, op_name: str) -> bool:
        """依存関係をチェックします。"""
        if op_name in self.status_cache:
            return True
        
        return all(dep in self.results for dep in self.dependency_map.get(op_name, []))
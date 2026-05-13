class OperationManager:
    # ... [省略] ...
    
    def _execute_operation(self, item: Any, op_name: str) -> Dict[str, Any]:
        """指定された操作を実行し、その結果を返します。"""
        operation = self.operations.get(op_name)
        if operation:
            try:
                return operation(item)
            except Exception as e:
                return {'success': False, 'error': f'操作 {op_name} の実行中にエラーが発生: {str(e)}'}
        return {'success': False, 'error': f'操作 {op_name} が見つかりません。'}

    def _log_error(self, op_name: str, item: Any, error: str) -> None:
        logging.error(f"エラー発生: '{error}' - 操作: '{op_name}' に対してアイテム: '{item}'")
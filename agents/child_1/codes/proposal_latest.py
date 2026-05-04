def improved_dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
    """選択した操作をデータに対して実行します。依存関係を考慮します。エラーハンドリングを改善。"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(self._execute_operation, item, op_name): (item, op_name)
            for item in data
            for op_name in chosen_operations if op_name in self.operations and self._check_dependencies(op_name)
        }

        for future in as_completed(futures):
            item, op_name = futures[future]
            result = None
            try:
                result = future.result()
            except Exception as e:
                logging.error(f"Error executing operation '{op_name}' for item '{item}': {str(e)}")
                result = {'item': item, 'operation': op_name, 'error': str(e), 'success': False}
            finally:
                with self.lock:
                    self.results.append(result)
                    if 'success' in result and result['success']:
                        self._update_progress(op_name)

def _improved_visualize_progress(self) -> None:
    """進捗をより視覚的に表現するメソッドを追加。"""
    total_operations = sum(self.current_progress.values())
    logging.info(f"全操作の進捗: {total_operations} / {len(self.operations)}")
    # ここで、グラフやSVGを使って進捗バーを視覚的に表示するロジックを追加
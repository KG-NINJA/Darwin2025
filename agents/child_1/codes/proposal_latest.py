def efficient_dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
    """選択した操作をデータに対して効率的に実行します。"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(self._execute_operation, item, op_name): (item, op_name)
            for item in data
            for op_name in chosen_operations if self._check_dependencies(op_name) and op_name in self.operations
        }

        for future in as_completed(futures):
            item, op_name = futures[future]
            try:
                result = future.result()
                if not result.get('success', False):
                    logging.error(f"Error executing operation '{op_name}' for item '{item}': {result.get('error')}")
            except Exception as e:
                logging.error(f"Unexpected error for '{op_name}' and '{item}': {str(e)}")
            else:
                with self.lock:
                    self.results.append(result)
                    if result['success']:
                        self._update_progress(op_name)

def _efficient_visualize_progress(self) -> None:
    """進捗の視覚化を効率的に行うメソッドを追加。"""
    total_operations = sum(self.current_progress.values())
    percentage_complete = (total_operations / len(self.operations)) * 100
    logging.info(f"進捗状況: {total_operations} / {len(self.operations)} - 完了率: {percentage_complete:.2f}%")
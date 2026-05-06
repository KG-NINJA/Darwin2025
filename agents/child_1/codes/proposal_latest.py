def creative_dynamic_run_operations(self, data: List[Any], chosen_operations: List[str], max_workers: int = 10) -> None:
    """選択した操作をデータに対して創造的に実行します。"""
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
                self._handle_result(item, op_name, result)
            except Exception as e:
                logging.error(f"Unexpected error for '{op_name}' and '{item}': {str(e)}")

    self._visualize_overall_progress()

def _handle_result(self, item, op_name, result):
    """結果を処理し、進捗を更新します。"""
    if result.get('success'):
        with self.lock:
            self.results.append(result)
            self._update_progress(op_name)
    else:
        logging.error(f"Operation '{op_name}' failed for item '{item}': {result.get('error')}")

def _visualize_overall_progress(self) -> None:
    """全体の進捗を視覚的に表示します。"""
    total_operations = sum(self.current_progress.values())
    percentage_complete = (total_operations / len(self.operations)) * 100
    logging.info(f"進捗状況: {total_operations} / {len(self.operations)} - 完了率: {percentage_complete:.2f}%")
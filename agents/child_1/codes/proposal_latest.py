class EnhancedOperationManager(OperationManager):
    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        
        # Validate data upfront
        valid_data, invalid_data = self.validate_data(data)

        if not valid_data:
            results["errors"].append("No valid data to process.")
            return results

        if invalid_data:
            results["errors"].extend(invalid_data)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
            for future in as_completed(future_to_data):
                try:
                    item_results = future.result()
                    results['results'].extend(item_results.get('results', []))
                    results['errors'].extend(item_results.get('errors', []))
                except Exception as e:
                    results['errors'].append(f"[ERROR] {str(e)} encountered during processing.")

        self._log_metrics()
        self._save_log_to_file()
        self._aggregate_metrics()

        return results

    def validate_data(self, data: List[Union[int, float]]) -> Tuple[List[Union[int, float]], List[str]]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [f"{item} is not a valid number." for item in data if not isinstance(item, (int, float))]
        return valid_data, invalid_data

    def _aggregate_metrics(self):
        """メトリクスを集約して定期的に記録する最適化を行います。"""
        metrics_data = {op.name: {"successes": op.success_count, "errors": op.error_count} for op in self.operations.values()}
        # Further processing or aggregation can be done here if needed
        print("\nAggregated summary of operations:", json.dumps(metrics_data, indent=2))
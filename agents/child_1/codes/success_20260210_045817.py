from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Tuple
import json

class EnhancedOperationManager:
    def __init__(self, max_workers: int):
        self.max_workers = max_workers
        self.operations = {}

    def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
        results = {"results": [], "errors": []}
        
        # データの検証を効率化
        valid_data, invalid_data = self.validate_data(data)
        if invalid_data:
            results["errors"].extend(invalid_data)

        if not valid_data:
            results["errors"].append("No valid data to process.")
            return results

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}

            for future in as_completed(future_to_data):
                try:
                    item_results = future.result()
                    results['results'].extend(item_results.get('results', []))
                    results['errors'].extend(item_results.get('errors', []))
                except Exception as e:
                    results['errors'].append(f"[ERROR] {str(e)} encountered during processing.")

        self._aggregate_metrics()
        self._log_metrics(results)

        return results

    def validate_data(self, data: List[Union[int, float]]) -> Tuple[List[Union[int, float]], List[str]]:
        valid_data = [item for item in data if isinstance(item, (int, float))]
        invalid_data = [f"{item} is not a valid number." for item in data if not isinstance(item, (int, float))]
        return valid_data, invalid_data

    def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> dict:
        # Processing logic for each item
        return {"results": [item], "errors": []}  # Example output

    def _aggregate_metrics(self):
        """全ての操作のメトリクスを集約して出力します。"""
        metrics_data = {op: {"successes": 0, "errors": 0} for op in self.operations}
        print("\nAggregated summary of operations:", json.dumps(metrics_data, indent=2))

    def _log_metrics(self, results: dict):
        """メトリクスを効率的にログ出力するメソッド。"""
        pass  # Implement log output logic

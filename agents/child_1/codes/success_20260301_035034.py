import logging
import json
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Callable


async def log_metrics(results: dict):
    # I/O効率化のため、非同期で結果を書き込む
    log_entry = {
        "results": results['results'],
        "errors": results['errors'],
        "timestamp": datetime.now().isoformat()
    }
    async with aiofiles.open('metrics_log.json', 'a') as log_file:
        await log_file.write(json.dumps(log_entry) + "\n")


def run_operations(self, data: List[Union[int, float]], chosen_operations: List[str]) -> dict:
    results = {"results": [], "errors": []}
    valid_data, invalid_data = self.validate_data(data)
    results["errors"].extend(invalid_data)

    if not valid_data:
        results["errors"].append("No valid data to process.")
        return results

    with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
        future_to_data = {executor.submit(self._process_item, item, chosen_operations): item for item in valid_data}
        for future in as_completed(future_to_data):
            item_results = future.result()
            results['results'].extend(item_results['results'])
            results['errors'].extend(item_results['errors'])

    asyncio.run(log_metrics(results))  # 新しい非同期ログ関数を呼び出す
    self._aggregate_metrics(results)
    return results

def _process_item(self, item: Union[int, float], chosen_operations: List[str]) -> dict:
    results = {"results": [], "errors": []}
    for op_name in chosen_operations:
        operation = self.operations.get(op_name)

        if operation is None:
            results['errors'].append(f"Warning: Operation '{op_name}' not registered. Skipping.")
            continue

        result = self._execute_with_retry(operation, item, op_name)
        
        if result['errors']:
            results['errors'].extend(result['errors'])
        else:
            results['results'].extend(result['results'])

    return results

def _execute_with_retry(self, operation: Callable, item: Union[int, float], op_name: str) -> dict:
    results = {"results": [], "errors": []}
    for attempt in range(self.retry_attempts):
        try:
            result = operation(item)
            results['results'].append(result)
            break 
        except Exception as e:
            error_message = f"Operation '{op_name}' failed: {e} (Attempt {attempt + 1})"
            logging.error(error_message)
            results['errors'].append(error_message)
            if attempt == self.retry_attempts - 1:
                results['errors'].append(f"Error: Operation '{op_name}' failed after {self.retry_attempts} attempts.")
    return results
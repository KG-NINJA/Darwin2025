from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

class Strategy:
    def execute(self):
        # 戦略の実行ロジックをここに実装
        logging.info("Executing strategy.")
        # ここでエラーを発生させる例
        # raise ValueError("Sample error")

class DynamicThreadPoolExecutor:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.active_futures = []

    def submit(self, fn, *args, **kwargs):
        future = self.executor.submit(fn, *args, **kwargs)
        self.active_futures.append(future)
        return future

    def shutdown(self):
        logging.info("Shutting down thread pool.")
        for future in self.active_futures:
            try:
                future.result()
            except ValueError as ve:
                logging.error(f"ValueError encountered: {str(ve)}")
            except Exception as e:
                logging.error(f"General error occurred: {str(e)}")
        self.executor.shutdown(wait=True)

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_list = []
        self.executed_strategies = set()

    def add_strategy(self, strategy: Strategy, condition=lambda: True) -> None:
        self.strategy_list.append((strategy, condition))
        logging.info(f"Registered strategy with condition: {condition.__name__}")

    def execute_strategies(self) -> None:
        with DynamicThreadPoolExecutor() as executor:
            futures = {}
            for strategy, condition in self.strategy_list:
                if condition() and strategy not in self.executed_strategies:
                    futures[executor.submit(strategy.execute)] = strategy
                    self.executed_strategies.add(strategy)

            while futures:
                for future in as_completed(futures):
                    strategy = futures.pop(future)
                    try:
                        future.result()
                        logging.info(f"Strategy '{strategy}' executed successfully.")
                    except Exception as e:
                        self.log_error(strategy, e)

    def log_error(self, strategy: Strategy, error: Exception) -> None:
        logging.error(f"Error occurred in strategy '{strategy}': {str(error)}")

    def monitor_resources(self):
        while True:
            # システムリソースの状態を監視するロジックをここに実装
            time.sleep(5)  # 5秒ごとにリソースをチェック
            logging.info("Monitoring resources...")

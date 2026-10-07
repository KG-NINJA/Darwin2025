from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class Strategy:
    def execute(self):
        # 戦略の実行ロジックをここに実装
        pass

class DynamicThreadPoolExecutor:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.active_futures = []

    def submit(self, fn, *args, **kwargs):
        future = self.executor.submit(fn, *args, **kwargs)
        self.active_futures.append(future)
        return future

    def shutdown(self):
        logging.info("スレッドプールのシャットダウンを開始します。")
        for future in self.active_futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"戦略の実行中にエラーが発生しました: {str(e)}")
        self.executor.shutdown(wait=True)

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_list = []  # 戦略のリストを保持
        self.executed_strategies = set()  # 実行済みの戦略を追跡するセット

    def add_strategy(self, strategy: Strategy, condition=lambda: True) -> None:
        self.strategy_list.append((strategy, condition))
        logging.info(f"戦略が登録されました。条件: {condition.__name__}")

    def execute_strategies(self) -> None:
        with DynamicThreadPoolExecutor() as executor:
            futures = {}
            for strategy, condition in self.strategy_list:
                if condition() and strategy not in self.executed_strategies:  # 条件と重複を確認
                    futures[executor.submit(strategy.execute)] = strategy
                    self.executed_strategies.add(strategy)

            for future in as_completed(futures):
                strategy = futures[future]
                try:
                    future.result()
                    logging.info(f"戦略 '{strategy}' が正常に実行されました。")
                except Exception as e:
                    self.log_error(strategy, e)

    def log_error(self, strategy: Strategy, error: Exception) -> None:
        logging.error(f"戦略 '{strategy}' の実行中にエラーが発生しました: {str(error)}")

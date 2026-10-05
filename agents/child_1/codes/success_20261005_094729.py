from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class Strategy:
    def execute(self):
        # 戦略の実行ロジックをここに実装
        pass

class DynamicThreadPoolExecutor:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
    
    def submit(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self):
        self.executor.shutdown(wait=True)

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}
        self.executed_strategies = set()  # 実行済みの戦略を追跡するセット

    def add_strategy(self, name: str, strategy: Strategy) -> None:
        if name in self.strategy_map:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        self.strategy_map[name] = strategy
        logging.info(f"戦略 '{name}' が登録されました。")

    def execute_strategies(self) -> None:
        with DynamicThreadPoolExecutor() as executor:
            futures = {}
            for name, strategy in self.strategy_map.items():
                if name not in self.executed_strategies:  # 重複を避ける
                    futures[executor.submit(strategy.execute)] = name
                    self.executed_strategies.add(name)

            for future in as_completed(futures):
                name = futures[future]
                try:
                    future.result()
                    logging.info(f"戦略 '{name}' が正常に実行されました。")
                except Exception as e:
                    self.log_error(name, e)

    def log_error(self, name: str, error: Exception) -> None:
        logging.error(f"戦略 '{name}' の実行中にエラーが発生しました: {str(error)}")

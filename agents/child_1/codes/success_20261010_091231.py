from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

class Strategy:
    def execute(self):
        # 戦略の実行ロジックをここに実装
        logging.info("Executing strategy.")
        raise ValueError("Sample error") 

class EnhancedStrategyExecutor:
    def __init__(self, max_workers=2):
        self.strategies = []
        self.max_workers = max_workers
    
    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)
        logging.info(f"Added strategy: {strategy.__class__.__name__}")
    
    def execute_strategies(self):
        if not self.strategies:
            logging.warning("No strategies to execute.")
            return

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(strategy.execute): strategy for strategy in self.strategies}
            for future in as_completed(futures):
                strategy = futures[future]
                self.handle_future(future, strategy)

    def handle_future(self, future, strategy):
        try:
            future.result()
            logging.info(f"Strategy '{strategy.__class__.__name__}' executed successfully.")
        except Exception as e:
            self.log_error(strategy, e)

    def log_error(self, strategy, error):
        logging.error(f"Error in strategy '{strategy.__class__.__name__}': {str(error)}")

# 使用例
executor = EnhancedStrategyExecutor(max_workers=3)
executor.add_strategy(Strategy())
executor.execute_strategies()
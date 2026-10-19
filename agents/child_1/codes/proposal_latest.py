import logging
from concurrent.futures import ThreadPoolExecutor

class Strategy:
    """全ての戦略の基底クラス"""
    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

class CreativeStrategy(Strategy):
    """創造性を発揮できる戦略のクラス"""
    def execute(self):
        try:
            logging.info("CreativeStrategy is executing.")
            # 具体的な実装を追加
            return "Creative result"
        except Exception as e:
            logging.error(f"Error occurred in CreativeStrategy: {e}")
            return None

class CompositeStrategy(Strategy):
    """複数の戦略を統合して実行する戦略クラス"""
    def __init__(self, *strategies):
        self.strategies = strategies

    def execute(self):
        results = []
        with ThreadPoolExecutor() as executor:
            future_results = {executor.submit(strategy.execute()): strategy for strategy in self.strategies}
            for future in future_results:
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error occurred in {future_results[future].__class__.__name__}: {e}")
        return results

class FlexibleStrategyExecutor:
    def __init__(self, max_workers=4):
        self.strategies = []
        self.max_workers = max_workers

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def execute_strategies(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_results = {executor.submit(strategy.execute()): strategy for strategy in self.strategies}
            for future in future_results:
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error occurred in {future_results[future].__class__.__name__}: {e}")

# 使用例
executor = FlexibleStrategyExecutor(max_workers=4)
executor.add_strategy(CreativeStrategy())
executor.add_strategy(CompositeStrategy(CreativeStrategy())) 
executor.execute_strategies()
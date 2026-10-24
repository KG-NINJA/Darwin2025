import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class Strategy:
    """全ての戦略の基底クラス"""
    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

class CreativeStrategy(Strategy):
    """創造性を発揮できる戦略のクラス"""
    def execute(self, variation=None):
        try:
            logging.info("CreativeStrategy is executing with variation: %s", variation)
            result = f"Creative result with variation {variation}" if variation else "Creative result"
            return result
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
            for future in as_completed(future_results):
                strategy = future_results[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error occurred in {strategy.__class__.__name__}: {e}")
        return results

class FlexibleStrategyExecutor:
    """戦略を動的に管理・実行するためのエグゼキュータ"""
    def __init__(self, max_workers=4):
        self.strategies = []
        self.max_workers = max_workers

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def execute_strategies(self):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_results = {executor.submit(strategy.execute()): strategy for strategy in self.strategies}
            for future in as_completed(future_results):
                strategy = future_results[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error occurred in {strategy.__class__.__name__}: {e}")

    def execute_with_order(self, strategy_order):
        """指定された順序で戦略を実行します"""
        results = []
        for strategy in strategy_order:
            result = strategy.execute()
            results.append(result)
        return results

# 使用例
executor = FlexibleStrategyExecutor(max_workers=4)
executor.add_strategy(CreativeStrategy())
executor.add_strategy(CompositeStrategy(CreativeStrategy()))

# 戦略を指定した順序で実行
strategy_order = [CreativeStrategy(), CompositeStrategy(CreativeStrategy())]
print(executor.execute_with_order(strategy_order))
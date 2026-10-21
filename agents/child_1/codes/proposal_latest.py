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
            # ユーザーが指定する独自のアルゴリズムを追加
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
                    
    def customize_strategy(self, strategy_class, variation):
        """戦略に対するカスタマイズを提供します"""
        strategy_instance = strategy_class()
        return strategy_instance.execute(variation)

# 使用例
executor = FlexibleStrategyExecutor(max_workers=4)
executor.add_strategy(CreativeStrategy())
executor.add_strategy(CompositeStrategy(CreativeStrategy()))
executor.execute_strategies()
# 戦略をカスタマイズして実行
print(executor.customize_strategy(CreativeStrategy, variation="High Creativity"))
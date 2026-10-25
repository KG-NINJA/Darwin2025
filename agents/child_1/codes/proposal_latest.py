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
            return f"Creative result with variation {variation}" if variation else "Creative result"
        except Exception as e:
            logging.error(f"Error occurred in CreativeStrategy: {e}")
            return None

class OrderedCompositeStrategy(Strategy):
    """依存関係を考慮した順序で戦略を実行するクラス"""
    def __init__(self, strategies_with_dependencies):
        self.strategies_with_dependencies = strategies_with_dependencies

    def execute(self):
        results = []
        with ThreadPoolExecutor() as executor:
            future_results = {}
            for strategy, dependencies in self.strategies_with_dependencies:
                for dependency in dependencies:
                    future_results[executor.submit(dependency.execute())] = dependency
                future_results[executor.submit(strategy.execute())] = strategy
            
            for future in as_completed(future_results):
                strategy = future_results[future]
                try:
                    results.append(future.result())
                except Exception as e:
                    logging.error(f"Error occurred in {strategy.__class__.__name__}: {e}")
        return results

# 使用例
dependent_strategies = [
    (CreativeStrategy(), []),  # 依存関係なし
    (CreativeStrategy(), [CreativeStrategy()])  # 依存関係あり
]

ordered_executor = OrderedCompositeStrategy(dependent_strategies)
print(ordered_executor.execute())
import logging

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
        except Exception as e:
            logging.error(f"Error occurred in CreativeStrategy: {e}")

class CompositeStrategy(Strategy):
    """複数の戦略を統合して実行する戦略クラス"""
    def __init__(self, *strategies):
        self.strategies = strategies

    def execute(self):
        results = []
        for strategy in self.strategies:
            try:
                logging.info(f"Executing strategy: {strategy.__class__.__name__}")
                results.append(strategy.execute())
            except Exception as e:
                logging.error(f"Error occurred in {strategy.__class__.__name__}: {e}")
        return results

class FlexibleStrategyExecutor:
    def __init__(self, max_workers=4):
        self.strategies = []
        self.max_workers = max_workers

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def execute_strategies(self):
        for strategy in self.strategies:
            strategy.execute()

# 使用例
executor = FlexibleStrategyExecutor(max_workers=4)
executor.add_strategy(CreativeStrategy())
executor.add_strategy(CompositeStrategy(CreativeStrategy()))  # SampleStrategy は未定義のため削除
executor.execute_strategies()
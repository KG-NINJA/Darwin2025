class CreativeStrategy(Strategy):
    """創造性を発揮できる戦略のクラス"""
    def execute(self):
        # 創造的な手法を用いた処理の実装
        logging.info("CreativeStrategy is executing.")
        # ここに具体的な実装を追加

class CompositeStrategy(Strategy):
    """複数の戦略を統合して実行する戦略クラス"""
    def __init__(self, *strategies):
        self.strategies = strategies

    def execute(self):
        results = []
        for strategy in self.strategies:
            logging.info(f"Executing strategy: {strategy.__class__.__name__}")
            results.append(strategy.execute())
        return results

# 使用例
executor = FlexibleStrategyExecutor(max_workers=4)
executor.add_strategy(CreativeStrategy())
executor.add_strategy(CompositeStrategy(SampleStrategy(), CreativeStrategy()))
executor.execute_strategies()
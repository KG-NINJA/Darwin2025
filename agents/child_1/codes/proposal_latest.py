import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class Strategy:
    """戦略の基底クラス"""
    def execute(self):
        """戦略を実行するメソッド"""
        raise NotImplementedError("このメソッドはサブクラスで実装されるべきです。")

class EnhancedStrategyExecutor:
    def __init__(self, max_workers=None):
        self.strategies = []
        self.max_workers = max_workers or self.get_dynamic_worker_count()
    
    def add_strategy(self, strategy: Strategy):
        """新しい戦略を追加"""
        self.strategies.append(strategy)
        logging.info(f"Added strategy: {strategy.__class__.__name__}")
    
    def execute_strategies(self):
        """すべての戦略を同時に実行"""
        if not self.strategies:
            logging.warning("No strategies to execute.")
            return

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(strategy.execute): strategy for strategy in self.strategies}
            for future in as_completed(futures):
                strategy = futures[future]
                self.handle_future(future, strategy)

    def handle_future(self, future, strategy):
        """Futureタスクの結果を処理"""
        try:
            future.result()
            logging.info(f"Strategy '{strategy.__class__.__name__}' executed successfully.")
        except Exception as e:
            self.log_error(strategy, e)

    def log_error(self, strategy, error):
        """エラーログを出力"""
        logging.error(f"Error in strategy '{strategy.__class__.__name__}': {str(error)}")

    def get_dynamic_worker_count(self):
        """動的にワーカースレッドの数を決定"""
        # 環境に応じたスレッド数を計算するロジックを追加可能
        return 5  # 例として5を返す

# 使用例
executor = EnhancedStrategyExecutor(max_workers=4)
executor.add_strategy(SampleStrategy())
executor.execute_strategies()
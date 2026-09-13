from abc import ABC, abstractmethod
import logging

class Strategy(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SampleStrategy(Strategy):
    def execute(self) -> None:
        pass

class AnotherStrategy(Strategy):
    def execute(self) -> None:
        pass

class StrategyFactory:
    valid_strategies = {
        "SampleStrategy": SampleStrategy,
        "AnotherStrategy": AnotherStrategy
    }

    @staticmethod
    def create_strategy(strategy_type: str) -> Strategy:
        try:
            if strategy_type in StrategyFactory.valid_strategies:
                return StrategyFactory.valid_strategies[strategy_type]()
            else:
                raise ValueError(f"Unknown strategy type: {strategy_type}")
        except Exception as e:
            logging.error(f"Strategy creation failed: {e}")
            raise

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 戦略を追加します。 """
        try:
            strategy = StrategyFactory.create_strategy(strategy_type)
            if name not in self.strategy_map:
                self.strategy_map[name] = strategy
                logging.info(f"戦略 '{name}' が追加されました。")
            else:
                logging.warning(f"戦略 '{name}' は既に存在します。")
        except ValueError as e:
            logging.error(e)

    def execute_strategy(self, name: str) -> None:
        """ 戦略を実行します。 """
        if name not in self.strategy_map:
            logging.error(f"戦略 '{name}' は未登録です。")
            return
        strategy = self.strategy_map[name]
        strategy.execute()
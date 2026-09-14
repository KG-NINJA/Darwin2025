from abc import ABC, abstractmethod
import logging

class Strategy(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SampleStrategy(Strategy):
    def execute(self) -> None:
        logging.info("SampleStrategy is executed.")

class AnotherStrategy(Strategy):
    def execute(self) -> None:
        logging.info("AnotherStrategy is executed.")

class StrategyFactory:
    valid_strategies = {
        "SampleStrategy": SampleStrategy,
        "AnotherStrategy": AnotherStrategy
    }

    @staticmethod
    def create_strategy(strategy_type: str) -> Strategy:
        strategy_class = StrategyFactory.valid_strategies.get(strategy_type)
        if not strategy_class:
            logging.error(f"Unknown strategy type: {strategy_type}")
            raise ValueError(f"Unknown strategy type: {strategy_type}")
        return strategy_class()

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 戦略を追加します。 """
        if name in self.strategy_map:
            logging.warning(f"戦略 '{name}' は既に存在します。")
            return
        
        try:
            self.strategy_map[name] = StrategyFactory.create_strategy(strategy_type)
            logging.info(f"戦略 '{name}' が追加されました。")
        except ValueError as e:
            logging.error(e)

    def execute_strategy(self, name: str) -> None:
        """ 戦略を実行します。 """
        strategy = self.strategy_map.get(name)
        if not strategy:
            logging.error(f"戦略 '{name}' は未登録です。")
            return
        
        strategy.execute()
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

class StrategyRegistry:
    _strategies = {}

    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_class: type) -> None:
        cls._strategies[strategy_type] = strategy_class

    @classmethod
    def get_strategy(cls, strategy_type: str) -> Strategy:
        strategy_class = cls._strategies.get(strategy_type)
        if strategy_class:
            return strategy_class()  # インスタンスを生成
        logging.error(f"Unknown strategy type: {strategy_type}")
        raise ValueError(f"Unknown strategy type: {strategy_type}")

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 新しい戦略を追加します。 """
        if name not in self.strategy_map:
            self.strategy_map[name] = StrategyRegistry.get_strategy(strategy_type)
            logging.info(f"戦略 '{name}' が追加されました。")
        else:
            logging.warning(f"戦略 '{name}' は既に存在します。")

    def execute_strategy(self, name: str) -> None:
        """ 異なる戦略を実行します。 """
        strategy = self.strategy_map.get(name)
        if strategy:
            strategy.execute()
        else:
            logging.error(f"戦略 '{name}' は未登録です。")

    def remove_strategy(self, name: str) -> None:
        """ 戦略を削除します。 """
        if name in self.strategy_map:
            del self.strategy_map[name]
            logging.info(f"戦略 '{name}' が削除されました。")
        else:
            logging.warning(f"戦略 '{name}' は存在しません。")

# 戦略の登録
StrategyRegistry.register_strategy("SampleStrategy", SampleStrategy)
StrategyRegistry.register_strategy("AnotherStrategy", AnotherStrategy)

# 使用例
processor = EnhancedDataProcessor()
processor.add_strategy("sample", "SampleStrategy")
processor.execute_strategy("sample")
processor.remove_strategy("sample")
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
    _instances = {}

    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_class: type) -> None:
        """ 戦略を登録し、既存の戦略との重複を避ける。 """
        if strategy_type not in cls._strategies:
            cls._strategies[strategy_type] = strategy_class
            logging.info(f"戦略 '{strategy_type}' が登録されました。")
        else:
            logging.warning(f"戦略 '{strategy_type}' は既に登録されています。")

    @classmethod
    def get_strategy(cls, strategy_type: str) -> Strategy:
        """ 戦略のインスタンスを取得、存在しなければエラーを報告。 """
        if strategy_type in cls._instances:
            return cls._instances[strategy_type]
        
        strategy_class = cls._strategies.get(strategy_type)
        if strategy_class:
            instance = strategy_class()
            cls._instances[strategy_type] = instance
            return instance
        logging.error(f"未知の戦略タイプ: {strategy_type}")
        raise ValueError(f"未知の戦略タイプ: {strategy_type}")

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 新しい戦略を追加します。 """
        if name not in self.strategy_map:
            try:
                self.strategy_map[name] = StrategyRegistry.get_strategy(strategy_type)
                logging.info(f"戦略 '{name}' が追加されました。")
            except ValueError as e:
                logging.error(f"エラー: {e}")
        else:
            logging.warning(f"戦略 '{name}' は既に存在します。")

    def execute_strategy(self, name: str) -> None:
        """ 戦略を実行します。 """
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
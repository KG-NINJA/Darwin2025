import importlib
import logging
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self) -> None:
        """ 戦略を実行するメソッド """
        pass

class StrategyRegistry:
    _strategies = {}
    
    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_module: str) -> None:
        """ 戦略をプラグインとして登録します。 """
        if strategy_type not in cls._strategies:
            try:
                module = importlib.import_module(strategy_module)
                cls._strategies[strategy_type] = module.Strategy()  # Get an instance
                logging.info(f"戦略 '{strategy_type}' が登録されました。")
            except ImportError as e:
                logging.error(f"モジュールのインポートに失敗しました: {e}")
            except Exception as e:
                logging.error(f"戦略の登録中にエラーが発生しました: {e}")
        else:
            logging.warning(f"戦略 '{strategy_type}' は既に登録されています。")

    @classmethod
    def get_strategy(cls, strategy_type: str) -> Strategy:
        """ 戦略のインスタンスを取得します。 """
        strategy = cls._strategies.get(strategy_type)
        if strategy:
            return strategy
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
                raise
            except Exception as e:
                logging.error(f"戦略の追加中にエラーが発生しました: {e}")
        else:
            logging.warning(f"戦略 '{name}' は既に存在します。")

    def execute_strategy(self, name: str) -> None:
        """ 戦略を実行します。 """
        strategy = self.strategy_map.get(name)
        if strategy:
            try:
                strategy.execute()
            except Exception as e:
                logging.error(f"戦略 '{name}' 実行中にエラーが発生しました: {e}")
        else:
            logging.error(f"戦略 '{name}' は未登録です。")

    def remove_strategy(self, name: str) -> None:
        """ 戦略を削除します。 """
        if name in self.strategy_map:
            del self.strategy_map[name]
            logging.info(f"戦略 '{name}' が削除されました。")
        else:
            logging.warning(f"戦略 '{name}' は存在しません。")

# 例として戦略をプラグインとして登録
# StrategyRegistry.register_strategy("SampleStrategy", "sample_strategy_module")
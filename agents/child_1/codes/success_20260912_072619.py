from abc import ABC, abstractmethod

class Strategy(ABC):  # 基本的な戦略インターフェース
    @abstractmethod
    def execute(self) -> None:
        pass

class SampleStrategy(Strategy):
    def execute(self) -> None:
        # 実行ロジック
        pass

class AnotherStrategy(Strategy):
    def execute(self) -> None:
        # 別の実行ロジック
        pass

class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str) -> Strategy:
        """ 指定されたタイプに基づいて戦略を生成します。 """
        if strategy_type == "SampleStrategy":
            return SampleStrategy()
        elif strategy_type == "AnotherStrategy":
            return AnotherStrategy()
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 戦略を追加します。 """
        try:
            strategy = StrategyFactory.create_strategy(strategy_type)
            if name not in self.strategy_map:
                new_node = Node(name, strategy)
                self.strategy_map[name] = new_node
                logging.info(f"戦略 '{name}' が追加されました。")
            else:
                logging.warning(f"戦略 '{name}' は既に存在します。")
        except ValueError as e:
            logging.error(e)

    # 他のメソッドは既存のまま
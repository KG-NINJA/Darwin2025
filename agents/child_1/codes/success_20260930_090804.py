import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class Strategy:
    def execute(self):
        pass

class StrategyRegistry:
    strategies = {}

    @classmethod
    def register_strategy(cls, name: str, strategy: Strategy) -> None:
        if name in cls.strategies:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        cls.strategies[name] = strategy
        logging.info(f"戦略 '{name}' が登録されました。")

    @classmethod
    def get_strategy(cls, name: str) -> Strategy:
        return cls.strategies.get(name)

    @classmethod
    def remove_strategy(cls, name: str) -> None:
        if name in cls.strategies:
            del cls.strategies[name]
            logging.info(f"戦略 '{name}' が削除されました。")
        else:
            logging.warning(f"戦略 '{name}' は未登録です。")

    @classmethod
    def list_strategies(cls) -> None:
        if cls.strategies:
            logging.info("登録されている戦略:")
            for name in cls.strategies.keys():
                logging.info(f"- {name}")
        else:
            logging.info("現在、登録されている戦略はありません。")

class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy: Strategy) -> None:
        """ 新しい戦略を追加します。 """
        if name in self.strategy_map:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        
        self.strategy_map[name] = strategy
        StrategyRegistry.register_strategy(name, strategy)

    def change_strategy_theme(self, name: str, new_strategy: Strategy) -> None:
        """ 戦略のテーマを変更します。 """
        if name not in self.strategy_map:
            logging.error(f"戦略 '{name}' は未登録です。エラー: 無効な戦略名です。")
            return
        
        self.strategy_map[name] = new_strategy
        StrategyRegistry.register_strategy(name, new_strategy)

    def execute_strategies(self) -> None:
        """ 登録された全戦略を同時に実行します。 """
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(strategy.execute): name for name, strategy in self.strategy_map.items()}
            for future in as_completed(futures):
                name = futures[future]
                try:
                    future.result()
                    logging.info(f"戦略 '{name}' が正常に実行されました。")
                except Exception as e:
                    logging.error(f"戦略 '{name}' の実行中にエラーが発生しました: {e}")

    def list_strategies(self) -> None:
        """ 登録済み戦略を表示します。 """
        StrategyRegistry.list_strategies()
class Strategy:
    def execute(self):
        pass

class StrategyRegistry:
    strategies = {}

    @classmethod
    def register_strategy(cls, name: str, strategy: Strategy) -> None:
        cls.strategies[name] = strategy

    @classmethod
    def get_strategy(cls, name: str) -> Strategy:
        return cls.strategies.get(name)

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
        logging.info(f"戦略 '{name}' が正常に追加されました。")

    def change_strategy_theme(self, name: str, new_strategy: Strategy) -> None:
        """ 戦略のテーマを変更します。 """
        if name not in self.strategy_map:
            logging.error(f"戦略 '{name}' は未登録です。")
            return
        
        logging.info(f"戦略 '{name}' のテーマを変更します。")
        self.strategy_map[name] = new_strategy
        StrategyRegistry.register_strategy(name, new_strategy)

    def execute_strategy(self, name: str) -> None:
        """ 戦略を実行します。 """
        strategy = self.strategy_map.get(name)
        if strategy:
            strategy.execute()
        else:
            logging.error(f"戦略 '{name}' は未登録です。")

    def list_strategies(self) -> None:
        """ 登録済み戦略を表示します。 """
        if self.strategy_map:
            logging.info("登録されている戦略:")
            logging.info("\n".join(f"- {name}" for name in self.strategy_map.keys()))
        else:
            logging.info("現在、登録されている戦略はありません。")
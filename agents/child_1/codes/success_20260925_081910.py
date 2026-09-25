class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 新しい戦略を追加します。 """
        if name in self.strategy_map:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        
        strategy = StrategyRegistry.get_strategy(strategy_type)
        if strategy is None:
            logging.error(f"無効な戦略タイプ: {strategy_type}")
            return
        
        self.strategy_map[name] = strategy
        logging.info(f"戦略 '{name}' が正常に追加されました。")

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
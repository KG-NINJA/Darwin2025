class EnhancedDataProcessor:
    def __init__(self):
        self.strategy_map = {}

    def list_strategies(self) -> None:
        """ 登録済み戦略を表示します。 """
        if self.strategy_map:
            logging.info("登録されている戦略:")
            for name in self.strategy_map.keys():
                logging.info(f"- {name}")
        else:
            logging.info("現在、登録されている戦略はありません。")

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 新しい戦略を追加します。 """
        if name not in self.strategy_map:
            try:
                self.strategy_map[name] = StrategyRegistry.get_strategy(strategy_type)
                logging.info(f"戦略 '{name}' が正常に追加されました。")
            except ValueError as e:
                logging.error(f"エラー: {e}")
            except Exception as e:
                logging.error(f"戦略の追加中にエラーが発生しました: {e}")
        else:
            logging.warning(f"戦略 '{name}' は既に登録されています。")

    # 省略: その他メソッドの定義

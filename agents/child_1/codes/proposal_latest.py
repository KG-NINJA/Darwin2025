class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type: str) -> Strategy:
        """ 指定されたタイプに基づいて戦略を生成します。 """
        if strategy_type == "SampleStrategy":
            return SampleStrategy()  #ここに他の戦略を追加
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

class EnhancedDataProcessor:
    # ... 既存のコード ...

    def add_strategy(self, name: str, strategy_type: str) -> None:
        """ 戦略を追加します。 """
        try:
            strategy = StrategyFactory.create_strategy(strategy_type)
            # 以降は既存のコードと同様
            if name not in self.strategy_map:
                logging.info(f"戦略を追加: {name}")
                new_node = Node(name, strategy)
                if self.tail:
                    self.tail.next = new_node
                    new_node.prev = self.tail
                else:
                    self.head = new_node
                self.tail = new_node
                self.strategy_map[name] = new_node
                logging.info(f"戦略 '{name}' が追加されました。")
            else:
                logging.warning(f"戦略 '{name}' は既に存在します。")
        except ValueError as e:
            logging.error(e)

    # ... その他の既存のメソッド ...
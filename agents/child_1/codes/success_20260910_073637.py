import logging
import asyncio
from typing import Callable, Dict, Any, List, Optional

# ロギングの設定
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class Strategy:
    def execute(self, data: Any) -> Any:
        """ 各戦略で実装されるべきメソッド """
        raise NotImplementedError("戦略の実行方法を定義してください。")

class SampleStrategy(Strategy):
    def execute(self, data: Any) -> Any:
        # データ処理のロジックを実装
        return f"Processed {data}"

class Node:
    def __init__(self, key: str, strategy: Strategy):
        self.key = key
        self.strategy = strategy
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class EnhancedDataProcessor:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.strategy_map: Dict[str, Node] = {}

    def add_strategy(self, name: str, strategy: Strategy) -> None:
        """ 戦略を追加します。 """
        if isinstance(strategy, Strategy):
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
        else:
            logging.error(f"無効な戦略が指定されました: {name}")

    async def execute_multiple_strategies(self, strategy_names: List[str], *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """ 複数の戦略を非同期的に実行します。 """
        tasks = []
        for name in strategy_names:
            strategy_node = self.strategy_map.get(name)
            if strategy_node:
                tasks.append(self._async_execute(strategy_node.strategy.execute, args, kwargs))
            else:
                logging.error(f"戦略 '{name}' が見つかりません。")
        return await asyncio.gather(*tasks)

    async def _async_execute(self, func: Callable, args: Any, kwargs: Any) -> Dict[str, Any]:
        """ 戦略の非同期実行処理を1元管理します。 """
        try:
            result = await func(*args, **kwargs)
            return {"result": result}
        except Exception as e:
            error_msg = f"エラーが発生しました: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}

    def remove_strategy(self, name: str) -> None:
        """ 戦略を削除します。 """
        node_to_remove = self.strategy_map.pop(name, None)
        if node_to_remove:
            if node_to_remove.prev:
                node_to_remove.prev.next = node_to_remove.next
            if node_to_remove.next:
                node_to_remove.next.prev = node_to_remove.prev
            if node_to_remove == self.head:
                self.head = node_to_remove.next
            if node_to_remove == self.tail:
                self.tail = node_to_remove.prev
            logging.info(f"戦略 '{name}' が削除されました。")
        else:
            logging.warning(f"戦略 '{name}' は存在しません。")

    def list_strategies(self) -> List[str]:
        """ 登録されている戦略のリストを取得します。 """
        return list(self.strategy_map.keys())
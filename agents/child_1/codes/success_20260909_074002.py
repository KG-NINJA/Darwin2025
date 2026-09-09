import logging
import asyncio
from typing import Callable, Dict, Any, List

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
        self.prev = None
        self.next = None

class EnhancedDataProcessor:
    def __init__(self):
        self.head = None
        self.tail = None
        self.strategy_map: Dict[str, Node] = {}

    def add_strategy(self, name: str, strategy: Strategy) -> None:
        """ 戦略を追加します。 """
        if isinstance(strategy, Strategy):
            if name not in self.strategy_map:
                logging.info(f"戦略の衝突チェックを実施中: {name}")
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

    async def execute_strategy(self, strategy_name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy_node = self.strategy_map.get(strategy_name)
        if strategy_node is None:
            error_msg = f"戦略 '{strategy_name}' が見つかりません。"
            logging.error(error_msg)
            return {"error": error_msg}

        result = await self._async_execute(strategy_node.strategy.execute, args, kwargs)
        return result

    async def _async_execute(self, func: Callable, args: Any, kwargs: Any) -> Dict[str, Any]:
        """ 戦略の非同期実行処理を1元管理します。 """
        try:
            result = await func(*args, **kwargs)
            logging.info(f"戦略の結果: {result}")
            return {"result": result}
        except Exception as e:
            error_msg = f"エラーが発生しました: {str(e)}"
            logging.error(f"戦略 '{func.__name__}' 実行中に{error_msg}")
            return {"error": error_msg}

    def list_strategies(self) -> List[str]:
        """ 登録されている戦略のリストを取得します。 """
        return list(self.strategy_map.keys())
import logging
import asyncio
from typing import Callable, Dict, Any, List

# ロギングの設定
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Callable[[Any], Any]] = {}

    def add_strategy(self, name: str, strategy: Callable[[Any], Any]) -> None:
        """ 戦略を追加します。 """
        if self._is_valid_strategy(strategy):
            if name not in self.strategies:
                self.strategies[name] = strategy
                logging.info(f"戦略 '{name}' が追加されました。")
            else:
                logging.warning(f"戦略 '{name}' は既に存在します。")
        else:
            logging.error(f"無効な戦略が指定されました: {name}")

    async def execute_strategy(self, strategy_name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            error_msg = f"戦略 '{strategy_name}' が見つかりません。"
            logging.error(error_msg)
            return {"error": error_msg}

        return await self._async_execute(strategy, args, kwargs)

    async def _async_execute(self, func: Callable, args: Any, kwargs: Any) -> Dict[str, Any]:
        """ 戦略の非同期実行処理を1元管理します。 """
        try:
            result = await asyncio.to_thread(func, *args, **kwargs)
            logging.info(f"戦略の結果: {result}")
            return {"result": result}
        except Exception as e:
            error_msg = f"エラーが発生しました: {str(e)}"
            logging.error(error_msg)
            return {"error": error_msg}

    def _is_valid_strategy(self, strategy: Callable[[Any], Any]) -> bool:
        """ 戦略が有効か確認します。 """
        return callable(strategy)

    def list_strategies(self) -> List[str]:
        """ 登録されている戦略のリストを取得します。 """
        return list(self.strategies.keys())
import logging
import asyncio
from typing import Callable, Dict, Any, List

# ロギングの設定
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class Strategy:
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """ 各戦略で実装されるべきメソッド """
        raise NotImplementedError("戦略の実行方法を定義してください。")

class SampleStrategy(Strategy):
    def execute(self, data: Any) -> Any:
        # データ処理のロジックを実装
        return f"Processed {data}"

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}

    def add_strategy(self, name: str, strategy: Strategy) -> None:
        """ 戦略を追加します。 """
        if isinstance(strategy, Strategy):
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

        return await self._async_execute(strategy.execute, args, kwargs)

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

    def list_strategies(self) -> List[str]:
        """ 登録されている戦略のリストを取得します。 """
        return list(self.strategies.keys())
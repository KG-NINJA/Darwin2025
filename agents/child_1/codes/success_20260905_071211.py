import logging
import threading
import asyncio
from typing import Callable, Dict, Any, List, Optional

# ロギングの設定
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class Strategy:
    def __init__(self, name: str, execute: Callable[[Any], Any], description: str = ""):
        self.name = name
        self.execute = execute
        self.description = description

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.lock = threading.Lock()

    def add_strategy(self, name: str, strategy: Callable[[Any], Any], description: str = "") -> None:
        """ 戦略を追加するメソッド、スレッドセーフを確保 """
        with self.lock:
            if self._is_valid_strategy(strategy):
                if name not in self.strategies:
                    self.strategies[name] = Strategy(name, strategy, description)
                    logging.info(f"戦略 '{name}' が追加されました: {description}")
                else:
                    logging.warning(f"戦略 '{name}' は既に存在します。")
            else:
                self._log_invalid_strategy(name)

    async def execute_strategy(self, strategy_name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            return self._log_and_create_error(strategy_name)

        # 非同期実行
        return await self._async_execute(strategy.execute, args, kwargs)

    async def _async_execute(self, func: Callable, args: Any, kwargs: Any) -> Dict[str, Any]:
        """ 戦略の非同期実行処理を一元化 """
        try:
            result = await asyncio.to_thread(func, *args, **kwargs)
            logging.info(f"戦略の結果: {result}")
            return {"result": result}
        except Exception as e:
            return self._log_and_create_error(str(e), strategy_name="")

    def _is_valid_strategy(self, strategy: Callable[[Any], Any]) -> bool:
        """ 戦略が有効か確認 """
        return callable(strategy)

    def _log_and_create_error(self, message: str, strategy_name: str = "") -> Dict[str, str]:
        """ エラーメッセージを生成し、ログに記録します。 """
        error_message = f"戦略 '{strategy_name}' 実行中にエラーまたは無効な戦略が発生しました: {message}"
        logging.error(error_message)
        return {"error": error_message}

    def list_strategies(self) -> List[Dict[str, Optional[str]]]:
        """ 登録されている戦略のリストを取得します。 """
        return [{"name": key, "description": strategy.description} for key, strategy in self.strategies.items()]
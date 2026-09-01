import logging
import threading
import asyncio
from typing import Callable, Dict, Any, Union, List

# ロギングの設定
logging.basicConfig(level=logging.INFO)

class Strategy:
    def __init__(self, name: str, execute: Callable, description: str = ""):
        self.name = name
        self.execute = execute
        self.description = description

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.lock = threading.Lock()

    def add_strategy(self, name: str, strategy: Callable, description: str = "") -> None:
        """ 戦略を追加するメソッド """
        if self._is_valid_strategy(strategy):
            with self.lock:
                if name not in self.strategies:  # 重複追加を防ぐ
                    self.strategies[name] = Strategy(name, strategy, description)
                    logging.info(f"戦略 '{name}' が追加されました: {description}")
                else:
                    logging.error(f"戦略 '{name}' は既に存在します。")

    async def execute_strategy(self, strategy_name: str, *args, **kwargs) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            return self._create_error_message(f"戦略 '{strategy_name}' は存在しません。")

        try:
            result = await asyncio.to_thread(strategy.execute, *args, **kwargs)
            logging.info(f"戦略 '{strategy_name}' の結果: {result}")
            return {"result": result}
        except Exception as e:
            logging.error(f"戦略 '{strategy_name}' 実行中にエラーが発生しました: {str(e)}")
            return self._create_error_message(f"戦略 '{strategy_name}' 実行中のエラーが発生しました: {str(e)}")

    def _is_valid_strategy(self, strategy: Callable) -> bool:
        """ 戦略が有効か確認 """
        return callable(strategy)

    def _create_error_message(self, message: str) -> Dict[str, str]:
        """ エラーメッセージを生成します。 """
        return {"error": message}

    def list_strategies(self) -> List[Dict[str, Union[str, Callable]]]:
        """ 登録されている戦略のリストを取得します。 """
        return [{"name": key, "description": strategy.description} for key, strategy in self.strategies.items()]
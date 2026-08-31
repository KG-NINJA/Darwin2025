import logging
import threading
import time
import asyncio
from typing import Callable, Dict, Any

# ロギングの設定
logging.basicConfig(level=logging.INFO)

class Strategy:
    def __init__(self, name: str, execute: Callable):
        self.name = name
        self.execute = execute

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.lock = threading.Lock()

    def _log_message(self, message: str, is_error: bool = False) -> None:
        """ ロギングを一元化します。 """
        if is_error:
            logging.error(message)
        else:
            logging.info(message)

    def add_strategy(self, name: str, strategy: Callable) -> None:
        """ 戦略を追加するメソッド """
        if self._is_valid_strategy(strategy):
            with self.lock:
                if name not in self.strategies:  # 重複追加を防ぐ
                    self.strategies[name] = Strategy(name, strategy)
                    self._log_message(f"戦略 '{name}' が追加されました。")
                else:
                    self._log_message(f"戦略 '{name}' は既に存在します。", True)

    async def execute_strategy(self, strategy_name: str, *args, **kwargs) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            return self._create_error_message(f"戦略 '{strategy_name}' は存在しません。")

        start_time = time.time()
        try:
            result = await asyncio.to_thread(strategy.execute, *args, **kwargs)
            self._log_message(f"戦略 '{strategy_name}' の結果: {result} (実行時間: {time.time() - start_time:.2f}秒)")
            return {"result": result}
        except Exception as e:
            self._log_message(f"戦略 '{strategy_name}' 実行中にエラーが発生しました: {str(e)}", True)
            return self._create_error_message(f"戦略 '{strategy_name}' 実行中のエラーが発生しました: {str(e)}")

    def _is_valid_strategy(self, strategy: Callable) -> bool:
        """ 戦略が有効か確認 """
        if not callable(strategy):
            self._log_message("戦略は呼び出し可能ではありません。", True)
            return False
        return True

    def _create_error_message(self, message: str) -> Dict[str, str]:
        """ エラーメッセージを生成します。 """
        return {"error": message}
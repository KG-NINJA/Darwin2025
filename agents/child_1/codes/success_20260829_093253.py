from typing import Dict, Any, List, Callable, Optional
import importlib
import asyncio
import logging
import threading

# ロギングの設定
logging.basicConfig(level=logging.INFO)

class Strategy:
    def __init__(self, name: str, execute: Callable):
        self.name = name
        self.execute = execute

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.lock = threading.Lock()  # ロックを追加

    def _log_message(self, message: str, is_error: bool = False) -> None:
        """ ロギングを一元化します。 """
        if is_error:
            logging.error(message)
        else:
            logging.info(message)

    def add_strategy(self, name: str, strategy: Callable) -> None:
        """ 戦略を追加するメソッド """
        if self._is_valid_strategy(strategy):
            with self.lock:  # ロックの適用
                self.strategies[name] = Strategy(name, strategy)
                self._log_message(f"戦略 '{name}' が追加されました。")
        else:
            self._log_message(f"戦略 '{name}' の追加に失敗しました。", True)

    def load_strategy(self, module_name: str, strategy_name: str) -> None:
        """ 外部モジュールから戦略を読み込みます。 """
        try:
            module = importlib.import_module(module_name)
            strategy_class = getattr(module, strategy_name)
            if callable(strategy_class):
                self.add_strategy(strategy_name, strategy_class())
            else:
                self._log_message(f"{strategy_name} は呼び出し可能ではありません。", True)
        except ImportError as e:
            self._log_message(f"モジュール '{module_name}' の読み込みに失敗しました: {str(e)}", True)
        except AttributeError:
            self._log_message(f"モジュール '{module_name}' に戦略 '{strategy_name}' が存在しません。", True)

    async def execute_strategy(self, strategy_name: str, *args, **kwargs) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。"""
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            return self._create_error_message(f"戦略 '{strategy_name}' は存在しません。")

        try:
            result = await asyncio.to_thread(strategy.execute, *args, **kwargs)
            self._log_message(f"戦略 '{strategy_name}' の結果: {result}")
            return {"result": result}
        except Exception as e:
            self._log_message(f"戦略 '{strategy_name}' 実行中にエラーが発生しました: {str(e)}", True)
            return self._create_error_message(f"戦略 '{strategy_name}' 実行中のエラーが発生しました: {str(e)}")

    def _is_valid_strategy(self, strategy: Callable) -> bool:
        """ 戦略が有効か確認 """
        if not callable(strategy):
            self._log_message(f"戦略は呼び出し可能ではありません。", True)
            return False
        return True

    def _create_error_message(self, message: str) -> Dict[str, str]:
        """ エラーメッセージを生成します。 """
        return {"error": message}
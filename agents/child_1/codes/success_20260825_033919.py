from typing import Dict, Any, List, Callable, Optional
import importlib
import asyncio
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies = {}

    def _create_error_message(self, message: str) -> Dict[str, str]:
        """ エラーメッセージを生成します。 """
        return {"error": message}
    
    def _get_strategy(self, name: str) -> Optional[Callable]:
        """ 戦略を取得するヘルパー関数 """
        strategy = self.strategies.get(name)
        if strategy is None:
            logging.error(f"戦略 '{name}' が存在しません。")
            return None
        return strategy

    def add_strategy(self, name: str, strategy: Callable) -> None:
        """ 戦略を追加するメソッド """
        if self._is_valid_strategy(name, strategy):
            self.strategies[name] = strategy
            logging.info(f"戦略 '{name}' が追加されました。")
        else:
            logging.error(f"戦略 '{name}' の追加に失敗しました。")

    def load_strategy(self, module_name: str, strategy_name: str) -> None:
        """ 外部モジュールから戦略を読み込みます。 """
        try:
            module = importlib.import_module(module_name)
            strategy_class = getattr(module, strategy_name)
            if callable(strategy_class):
                self.add_strategy(strategy_name, strategy_class())
            else:
                logging.error(f"{strategy_name} は呼び出し可能ではありません。")
        except ImportError:
            logging.error(f"モジュール '{module_name}' の読み込みに失敗しました。")
        except AttributeError:
            logging.error(f"モジュール '{module_name}' に戦略 '{strategy_name}' が存在しません。")

    async def execute_strategy(self, strategy_name: str, data: List[float]) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。"""
        strategy = self._get_strategy(strategy_name)
        if strategy is None:
            return self._create_error_message(f"戦略 '{strategy_name}' は存在しません。")
        if not isinstance(data, list):
            logging.error("データはリスト型でなければなりません。")
            return self._create_error_message("データはリスト型でなければなりません。")
        try:
            result = await asyncio.to_thread(strategy.execute, data)
            logging.info(f"戦略 '{strategy_name}' の結果: {result}")
            return {"result": result}
        except Exception as e:
            logging.error(f"戦略 '{strategy_name}' 実行中にエラーが発生しました: {e}")
            return self._create_error_message("戦略実行中のエラーが発生しました。")

    def _is_valid_strategy(self, name: str, strategy: Callable) -> bool:
        """ 戦略が有効か確認 """
        if not callable(strategy):
            logging.error(f"戦略 '{name}' は呼び出し可能ではありません。")
            return False
        return True
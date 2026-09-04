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
                if name not in self.strategies:  # 重複追加を防ぐ
                    self.strategies[name] = Strategy(name, strategy, description)
                    logging.info(f"戦略 '{name}' が追加されました: {description}")
                else:
                    logging.warning(f"戦略 '{name}' は既に存在します。")
            else:
                logging.error(f"無効な戦略が渡されました: {name}")

    async def execute_strategy(self, strategy_name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """ 指定した戦略を非同期的に実行します。 """
        strategy = self.strategies.get(strategy_name)
        if strategy is None:
            error_message = f"戦略 '{strategy_name}' は存在しません。"
            logging.error(error_message)
            return self._create_error_message(error_message)

        try:
            result = await asyncio.to_thread(strategy.execute, *args, **kwargs)
            logging.info(f"戦略 '{strategy_name}' の結果: {result}")
            return {"result": result}
        except Exception as e:
            error_message = f"戦略 '{strategy_name}' 実行中にエラーが発生しました: {str(e)}"
            logging.error(error_message)
            return self._create_error_message(error_message)

    def _is_valid_strategy(self, strategy: Callable[[Any], Any]) -> bool:
        """ 戦略が有効か確認 """
        return callable(strategy)

    def _create_error_message(self, message: str) -> Dict[str, str]:
        """ エラーメッセージを生成します。 """
        return {"error": message}

    def list_strategies(self) -> List[Dict[str, Optional[str]]]:
        """ 登録されている戦略のリストを取得します。 """
        return [{"name": key, "description": strategy.description} for key, strategy in self.strategies.items()]
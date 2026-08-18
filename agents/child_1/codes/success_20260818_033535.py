from typing import List, Dict, Any, Protocol, Callable

class Strategy(Protocol):
    def execute(self, data: List[float]) -> Dict[str, Any]:
        ...

class EnhancedDataProcessor:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}

    def add_strategy(self, name: str, strategy: Strategy):
        if self._is_valid_strategy(name, strategy):
            self.strategies[name] = strategy
            print(f"戦略 '{name}' が追加されました。")

    def load_strategy(self, module_name: str, strategy_name: str):
        """外部モジュールから戦略を読み込みます。"""
        try:
            module = importlib.import_module(module_name)
            strategy = getattr(module, strategy_name, None)
            self.add_strategy(strategy_name, strategy())
        except ImportError as e:
            print(f"[ERROR] モジュール '{module_name}' の読み込みに失敗しました: {str(e)}")
        except AttributeError:
            print(f"[ERROR] モジュール '{module_name}' に戦略 '{strategy_name}' が存在しません。")

    def execute_strategy(self, strategy_name: str, data: Any) -> Dict[str, Any]:
        """指定した戦略を実行します。"""
        if not self._is_strategy_available(strategy_name):
            return self._create_error_message(f"戦略 '{strategy_name}' が存在しません。")
        if not isinstance(data, list):
            return self._create_error_message("データはリスト型でなければなりません。")
        return self.strategies[strategy_name].execute(data)

    def _create_error_message(self, message: str) -> Dict[str, Any]:
        return {'error': message}

    def _is_valid_strategy(self, name: str, strategy: Strategy) -> bool:
        if not callable(strategy.execute):
            print("[ERROR] 戦略は呼び出し可能である必要があります。")
            return False
        if name in self.strategies:
            print(f"[ERROR] 戦略 '{name}' はすでに存在します。")
            return False
        return True

    def _is_strategy_available(self, name: str) -> bool:
        """戦略の存在確認を行います。"""
        return name in self.strategies

class MeanStrategy:
    def execute(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {'error': "データが空です。"}
        return {'mean': sum(data) / len(data)}

class MedianStrategy:
    def execute(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {'error': "データが空です。"}
        sorted_data = sorted(data)
        mid = len(sorted_data) // 2
        return {
            'median': (sorted_data[mid - 1] + sorted_data[mid]) / 2 if len(sorted_data) % 2 == 0 else sorted_data[mid]
        }

async def main():
    data_processor = EnhancedDataProcessor()
    data_processor.add_strategy('mean', MeanStrategy())
    data_processor.add_strategy('median', MedianStrategy())

    print("利用可能な戦略:", list(data_processor.strategies.keys()))

    results_mean = data_processor.execute_strategy('mean', [1, 2, 3, 4, 5])
    results_median = data_processor.execute_strategy('median', [1, 2, 3, 4, 5])
    
    print("Mean結果:", results_mean)
    print("Median結果:", results_median)

# asyncio.run(main())
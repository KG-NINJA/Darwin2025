class EnhancedDataProcessor:
    
    def _get_strategy(self, name: str):
        """ 戦略を取得するヘルパー関数 """
        strategy = self.strategies.get(name)
        if not strategy:
            return self._create_error_message(f"戦略 '{name}' が存在しません。")
        return strategy

    def add_strategy(self, name: str, strategy: Strategy):
        if self._is_valid_strategy(name, strategy):
            self.strategies[name] = strategy
            print(f"戦略 '{name}' が追加されました。")
        
    def load_strategy(self, module_name: str, strategy_name: str):
        """外部モジュールから戦略を読み込みます。"""
        try:
            module = importlib.import_module(module_name)
            strategy_class = getattr(module, strategy_name)
            strategy_instance = strategy_class() if callable(strategy_class) else None
            return self.add_strategy(strategy_name, strategy_instance) if strategy_instance else self._create_error_message(f"{strategy_name} は呼び出し可能ではありません。")
        except ImportError:
            return self._create_error_message(f"モジュール '{module_name}' の読み込みに失敗しました。")
        except AttributeError:
            return self._create_error_message(f"モジュール '{module_name}' に戦略 '{strategy_name}' が存在しません。")

    async def execute_strategy(self, strategy_name: str, data: List[float]) -> Dict[str, Any]:
        """指定した戦略を非同期的に実行します。"""
        strategy = self._get_strategy(strategy_name)
        if "error" in strategy:
            return strategy
        if not isinstance(data, list):
            return self._create_error_message("データはリスト型でなければなりません。")
        return await asyncio.to_thread(strategy.execute, data)

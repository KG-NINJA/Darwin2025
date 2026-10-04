from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class Strategy:
    def execute(self):
        # 戦略の実行ロジック
        pass

class VersionedStrategy:
    def __init__(self):
        self.versions = {}
        self.dependencies = []  # 新しく追加された依存戦略

    def add_version(self, version: str, strategy: Strategy):
        if version in self.versions:
            logging.warning(f"戦略のバージョン '{version}' は既に存在します。")
            return
        self.versions[version] = strategy
        logging.info(f"戦略 '{version}' が追加されました。")

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def get_version(self, version: str) -> Strategy:
        return self.versions.get(version)

class StrategyRegistry:
    strategies = {}

    @classmethod
    def register_strategy(cls, name: str, strategy: VersionedStrategy) -> None:
        if name in cls.strategies:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        cls.strategies[name] = strategy
        logging.info(f"戦略 '{name}' が登録されました。")

class EnhancedDataProcessor:
    def __init__(self, max_workers=4):
        self.strategy_map = {}
        self.max_workers = max_workers  # スレッドプールの最大数

    def add_strategy(self, name: str, strategy: VersionedStrategy) -> None:
        if name in self.strategy_map:
            logging.warning(f"戦略 '{name}' は既に登録されています。")
            return
        self.strategy_map[name] = strategy
        StrategyRegistry.register_strategy(name, strategy)

    def execute_strategies(self) -> None:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for name, strategy in self.strategy_map.items():
                for version in strategy.versions.values():
                    # 依存関係を考慮する
                    dependencies_executed = [executor.submit(dep.execute) for dep in strategy.dependencies]
                    futures[executor.submit(version.execute, dependencies_executed)] = (name, version)
            for future in as_completed(futures):
                name, version = futures[future]
                try:
                    future.result()
                    logging.info(f"戦略 '{name}' のバージョンが正常に実行されました。")
                except Exception as e:
                    self.log_error(name, e)

    def log_error(self, name: str, error: Exception) -> None:
        logging.error(f"戦略 '{name}' の実行中にエラーが発生しました: {str(error)}")
        logging.error(f"詳細: {error.__class__.__name__} - {error}")

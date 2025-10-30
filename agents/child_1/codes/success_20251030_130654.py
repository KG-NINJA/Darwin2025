class Operation:
    def execute(self, data):
        raise NotImplementedError("このメソッドはオーバーライドされるべきです。")


class DoubleOperation(Operation):
    def execute(self, data):
        self.validate_input(data)
        return [item * 2 for item in data if item > 0]

    @staticmethod
    def validate_input(data):
        if not all(isinstance(i, (int, float)) for i in data):
            raise ValueError("すべての要素は数値である必要があります。")


class SquareOperation(Operation):
    def execute(self, data):
        self.validate_input(data)
        return [item ** 2 for item in data if item > 0]

    @staticmethod
    def validate_input(data):
        if not all(isinstance(i, (int, float)) for i in data):
            raise ValueError("すべての要素は数値である必要があります。")


class IncrementOperation(Operation):
    def execute(self, data):
        self.validate_input(data)
        return [item + 1 for item in data if item > 0]

    @staticmethod
    def validate_input(data):
        if not all(isinstance(i, (int, float)) for i in data):
            raise ValueError("すべての要素は数値である必要があります。")


class CreativeAlgorithm:
    def __init__(self, operation: Operation):
        self.operation = operation

    def process(self, data):
        return self.operation.execute(data)
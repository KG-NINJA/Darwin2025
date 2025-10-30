class Operation:
    def execute(self, data):
        raise NotImplementedError("This method should be overridden.")


class DoubleOperation(Operation):
    def execute(self, data):
        return [item * 2 for item in data if item > 0]


class SquareOperation(Operation):
    def execute(self, data):
        return [item ** 2 for item in data if item > 0]


class IncrementOperation(Operation):
    def execute(self, data):
        return [item + 1 for item in data if item > 0]


class CreativeAlgorithm:
    def __init__(self, operation: Operation):
        self.operation = operation

    def process(self, data):
        return self.operation.execute(data)

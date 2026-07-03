import logging
from typing import Callable

class SimpleOperation:
    def __init__(self, func: Callable):
        self.func = func

    def execute(self):
        try:
            result = self.func()
            logging.info(f"Operation completed successfully: {result}")
            return result
        except Exception as e:
            logging.error(f"Operation failed: {str(e)}")
            return None

# Example of improving a specific operation
def sample_operation():
    return "Operation done successfully!"

# Usage
operation = SimpleOperation(sample_operation)
operation.execute()
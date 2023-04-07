from typing import Callable


class Conditional:
    def __init__(
        self, operation: Callable, *args, elseop: Callable = None, checker: Callable
    ):
        self.operation = operation
        self.checker = checker
        if elseop is None:
            self.else_operation = lambda x: x
        else:
            self.else_operation = elseop

    def __call__(self, arg) -> object:
        if self.checker(arg):
            return self.operation(arg)
        else:
            return self.else_operation(arg)

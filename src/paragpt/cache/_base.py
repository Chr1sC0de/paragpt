from abc import abstractmethod
from typing import Callable
import pathlib as pt


class Base:
    cache_file: pt.Path

    def __init__(self, cache_file: pt.Path, operator: Callable):
        if cache_file is not None:
            self.cache_file = pt.Path(cache_file)
        else:
            self.cache_file = None
        self.operator = operator

    @abstractmethod
    def cache_loader(self, cache_file: pt.Path) -> object:
        ...

    @abstractmethod
    def cache_creator(self, obj: object, cache_file: pt.Path) -> None:
        ...

    def __call__(self, obj: object) -> object:
        if self.cache_file is not None:
            if self.cache_file.exists():
                return self.cache_loader(self.cache_file)
        output = self.operator(obj)
        if self.cache_file is not None:
            self.cache_creator(output, self.cache_file)
        return output

import pathlib as pt
from ._base import Base

class String(Base):

    def cache_loader(self, cache_file: pt.Path) -> str:
        with open(cache_file, 'r') as f:
            s = f.read()
        return s

    def cache_creator(self, arg: str, cache_file: pt.Path) -> None:
        with open(cache_file, "w") as f:
            f.write(arg)

    def __call__(self, obj: object ) -> str:
        return super().__call__(obj)

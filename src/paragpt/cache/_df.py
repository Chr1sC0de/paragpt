from ._base import Base
from typing import Callable
import pathlib as pt
import pandas as pd


class DataFrame(Base):
    def cache_loader(self, cache_file: pt.Path) -> pd.DataFrame:
        return pd.read_parquet(cache_file)

    def cache_creator(self, df: pd.DataFrame, cache_file: pt.Path):
        df.to_parquet(cache_file)

    def __call__(self, obj: object) -> pd.DataFrame:
        return super().__call__(obj)

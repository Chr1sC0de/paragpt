from typing import Callable, List
import pathlib as pt


class Pipeline:
    def __init__(self, *operations):
        self.operations = operations

    def __call__(self, input):
        transformed = input
        for operation in self.operations:
            transformed = operation(transformed)
        return transformed


def extract(extractable: object, extractor: Callable) -> object:
    return extractor(extractable)


def transform(transformable: object, *transformations: List[Callable]) -> object:
    for transform in transformations:
        transformable = transform(transformable)
    return transformable


def load(loadable: object, loader: Callable) -> object:
    return loader(loadable)

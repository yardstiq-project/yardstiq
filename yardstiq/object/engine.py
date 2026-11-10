from typing import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Engine:
    """"""

    name: str
    function: Callable

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class EngineRegistry:
    """EngineRegistry is a class that contains a registry of engines.
    It allows for the registration and retrieval of engines by name."""

    _engines = {}

    def register_engine(cls, engine: Engine):
        cls._engines[engine.name] = engine

    def get_engine(cls, name: str):
        if name in cls._engines:
            return cls._engines[name]
        raise KeyError(
            f"Engine'{name}' is not registered. Available engines: {list(cls._engines.keys())}"
        )

    def __getitem__(cls, name: str):
        return cls.get_engine(name)

    def get_engines(cls):
        return cls._engines.keys()

from typing import Callable
from dataclasses import dataclass
from yardstiq.registry import algorithm_database


@dataclass(frozen=True)
class Algorithm:
    """"""

    name: str
    problem: str
    version: str
    func: Callable
    hash: str = None
    id: str = "Not registered"

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def register(self):
        algorithm_database.register_algorithm(self)

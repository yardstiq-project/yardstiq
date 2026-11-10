from typing import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Algorithm:
    """"""

    problem: str
    func: Callable
    version: str

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class AlgorithmRegistry:
    """AlgorithmRegistry is a registry that holds all the algorithms registered in the system."""

    _algorithms = {}

    def register_algorithm(cls, algo: Algorithm):
        """Register an algorithm in the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm.
            func (callable): The function that implements the algorithm.
            version (str, optional): The version of the algorithm. Defaults to None.
        """
        cls._algorithms[algo.problem] = algo

    def get_algorithm(cls, problem: str) -> callable:
        """Get an algorithm from the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm."""
        if problem in cls._algorithms:
            return cls._algorithms[problem]
        raise KeyError(f"Problem: '{problem}' is not registered.")

    def __getitem__(cls, problem):
        return cls.get_algorithm(problem)

    def get_algorithms(cls):
        """Get all registered algorithms."""
        return cls._algorithms.keys()

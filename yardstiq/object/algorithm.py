from typing import Callable
from dataclasses import dataclass, replace
from .module import Module


@dataclass(frozen=True)
class Algorithm:
    """"""

    name: str
    problem: str
    version: str
    func: Callable
    hash: str = None
    local: bool = False
    id: str = "Not registered"

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class AlgorithmRegistry:
    """AlgorithmRegistry is a registry that holds all the algorithms registered in the system."""

    _algorithms: dict[str, list[Algorithm]] = {}

    def register_algorithm(cls, algo: Algorithm):
        """Register an algorithm in the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm.
            func (callable): The function that implements the algorithm.
            version (str, optional): The version of the algorithm. Defaults to None.
        """
        lst = cls._algorithms.setdefault(algo.problem, [])
        existing_versions = {alg.version for alg in lst}

        base_version = algo.version
        new_version = base_version
        counter = 1

        while new_version in existing_versions:
            new_version = f"{base_version}.{counter}"
            counter += 1

        names = algo.name.split(":")
        names[-1] = new_version

        name = ":".join(names)
        if new_version != algo.version:
            algo = replace(algo, version=new_version, name=name)

        lst.append(algo)

    def get_algorithm(cls, problem: str) -> list[Algorithm]:
        """Get an algorithm from the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm."""
        if problem in cls._algorithms.keys():
            return cls._algorithms[problem]
        raise KeyError(f"Problem: '{problem}' is not registered.")

    def __getitem__(cls, problem) -> list[Algorithm]:
        return cls.get_algorithm(problem)

    def get_algorithms(cls) -> dict[str, list[Algorithm]]:
        """Get all registered algorithms."""
        return cls._algorithms

    def get_new_algos(cls) -> list[Algorithm]:
        """Get all algorithms imported"""
        return [
            algo
            for algos_list in cls._algorithms.values()
            for algo in algos_list
            if not algo.local
        ]

    def clear(cls):
        cls._algorithms = {}

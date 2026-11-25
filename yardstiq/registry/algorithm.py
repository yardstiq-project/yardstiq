from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yardstiq.object import Algorithm

from dataclasses import replace


class AlgorithmRegistry:
    """AlgorithmRegistry is a registry that holds all the algorithms registered in the system."""

    _algorithms: dict[str, list[Algorithm]] = {}

    def register_algorithm(cls, algorithm: Algorithm):
        """Register an algorithm in the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm.
            func (callable): The function that implements the algorithm.
            version (str, optional): The version of the algorithm. Defaults to None.
        """
        lst = cls._algorithms.setdefault(algorithm.problem, [])
        existing_versions = {alg.version for alg in lst}

        base_version = algorithm.version
        new_version = base_version
        counter = 1

        while new_version in existing_versions:
            new_version = f"{base_version}.{counter}"
            counter += 1

        names = algorithm.name.split(":")
        names[-1] = new_version

        name = ":".join(names)
        if new_version != algorithm.version:
            algorithm = replace(algorithm, version=new_version, name=name)

        lst.append(algorithm)

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

    def clear(cls):
        cls._algorithms = {}

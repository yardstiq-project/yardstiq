from functools import wraps
from typing import Callable

def algorithm(problem: str = None, version: str = None ):
    """algorithm decorator to register an algorithm in the AlgorithmRegistry.

    Args:
        problem (str, optional): The problem the algorithm solves. Defaults to the function's name.
        version (str, optional): The version of the algorithm. Defaults to None.
    """

    if version is None or not isinstance(version, str):
        raise TypeError(f"Algorithm must provide a version string.")
    
    def decorator_algorithm(func: Callable):

        algorithm_name = problem if problem else func.__name__
        if algorithm_name in AlgorithmRegistry.get_algorithms():
            raise ValueError(f"Algorithm '{algorithm_name}' is already registered. Please use a different problem name.")
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                raise TypeError(f"Algorithm '{func.__name__}' must return a string containing the source code, but returned: {type(result).__name__}")
            return result

        AlgorithmRegistry.register_algorithm(algorithm_name, wrapper, version=version)

        return wrapper

    return decorator_algorithm


class AlgorithmRegistry:
    """AlgorithmRegistry is a registry that holds all the algorithms registered in the system."""

    _algorithms = {}

    @classmethod
    def register_algorithm(cls, name: str, func: callable, version: str = None):
        """Register an algorithm in the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm.
            func (callable): The function that implements the algorithm.
            version (str, optional): The version of the algorithm. Defaults to None.
        """
        cls._algorithms[name] = (func, version)

    @classmethod
    def get_algorithm(cls, name: str) -> callable:
        """Get an algorithm from the AlgorithmRegistry.

        Args:
            name (str): The name of the algorithm."""
        return cls._algorithms.get(name)

    @classmethod
    def __class_getitem__(cls, name):
        if name not in cls._algorithms:
            raise KeyError(f"Algorithm '{name}' is not registered. Available algorithms: {list(cls._algorithms.keys())}")
        return cls._algorithms[name]

    @classmethod
    def get_algorithms(cls):
        """Get all registered algorithms."""
        return cls._algorithms.keys()

from typing import Callable

from yardstiq.object import Algorithm
from yardstiq.object import Module
from yardstiq.registry import register_algorithm


def algorithm(problem: str, version: str = None):
    """Algorithm decorator to register an algorithm in the AlgorithmRegistry.

    Args:
        problem (str, optional): The problem the algorithm solves. Defaults to the function's name.
        version (str, optional): The version of the algorithm. Defaults to None.
    """

    if version is None or not isinstance(version, str):
        raise TypeError(f"Algorithm must provide a version string.")

    def decorator_algorithm(func: Callable):

        def wrapper(*args, **kwargs) -> list[Module]:
            result = func(*args, **kwargs)
            if not isinstance(result, list) or not all(
                isinstance(item, Module) for item in result
            ):
                raise TypeError(
                    f"Algorithm '{func.__name__}' must return a list containing modules, but returned: {type(result).__name__}"
                )
            return result

        name = ":".join([problem, func.__name__, version])
        version_ = func.__name__ + ":" + version
        algorithm_object = Algorithm(
            problem=problem,
            func=wrapper,
            version=version_,
            name=name,
        )
        register_algorithm(algorithm_object)
        return algorithm_object

    return decorator_algorithm

from functools import wraps
from typing import Callable
from yardstiq.object import algorithm_database
from yardstiq.object.algorithm import Algorithm
from yardstiq.object.module import Module


def algorithm(
    problem: str = None, version: str = None, local: bool = False, info: list = None
):
    """Algorithm decorator to register an algorithm in the AlgorithmRegistry.

    Args:
        problem (str, optional): The problem the algorithm solves. Defaults to the function's name.
        version (str, optional): The version of the algorithm. Defaults to None.
    """

    if version is None or not isinstance(version, str):
        raise TypeError(f"Algorithm must provide a version string.")

    def decorator_algorithm(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs) -> list[Module]:
            result = func(*args, **kwargs)
            if not isinstance(result, list) or not all(
                isinstance(item, Module) for item in result
            ):
                raise TypeError(
                    f"Algorithm '{func.__name__}' must return a list containing modules, but returned: {type(result).__name__}"
                )
            return result

        lst = wrapper(None)
        req = {}
        for module in lst:
            for cle, val in module.qall_args.items():
                if cle not in req:
                    req[cle] = val
                elif cle.startswith("max_"):
                    req[cle] = min(req[cle], val)
                elif cle.startswith("min_"):
                    req[cle] = max(req[cle], val)

        name = ":".join([problem, version, *info])
        algo = Algorithm(
            problem=problem,
            func=wrapper,
            version=version,
            local=local,
            modules=lst,
            requirements=req,
            info=info,
            name=name,
        )
        algorithm_database.register_algorithm(algo)
        return algo

    return decorator_algorithm

from functools import wraps
from yardstiq.object.workflow import WorkflowRun, WorkflowInfo
from typing import Callable
from yardstiq.object.engine import Engine
from yardstiq.object import engine_database


def engine(name: str = None):
    """engine decorator to register an engine in the EngineRegistry. It can be used with or without parameters.

    Args:
        func_or_name (callable or str, optional): The function to be decorated, OR the name of the engine.
        **kwargs: Additional keyword arguments to be passed to the engine function.
    """

    def decorator_engine(func: Callable):
        """decorator function to register an engine in the EngineRegistry."""

        engine_name = name if isinstance(name, str) else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function that checks the return type of the engine function is a WorkflowRun."""
            if not isinstance(*args, WorkflowInfo):
                raise TypeError(
                    f"Engine '{func.__name__}' only accepts WorkflowInfo as an input, got: {type(*args).__name__}"
                )
            result = func(*args, **kwargs)
            if not isinstance(result, WorkflowRun):
                raise TypeError(
                    f"Engine '{func.__name__}' must return a WorkflowRun, got: {type(result).__name__}"
                )
            return result

        eng = Engine(engine_name, wrapper)
        engine_database.register_engine(eng)
        return eng

    return decorator_engine

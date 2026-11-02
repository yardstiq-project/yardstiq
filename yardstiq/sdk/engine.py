from functools import wraps
from typing import Optional, Callable
from yardstiq.object.workflow import WorkflowRun

from functools import wraps
from typing import Optional, Callable, Union

from yardstiq.object.workflow import WorkflowRun

def engine(func_or_name: Union[Callable, str, None] = None, **kwargs):
    """engine decorator to register an engine in the EngineRegistry. It can be used with or without parameters.
    
    Args:
        func_or_name (callable or str, optional): The function to be decorated, OR the name of the engine.
        **kwargs: Additional keyword arguments to be passed to the engine function.
    """
    
    name = func_or_name if isinstance(func_or_name, str) else kwargs.get("name")

    def decorator_engine(f: Callable):
        """decorator function to register an engine in the EngineRegistry."""

        @wraps(f)
        def wrapper(*args, **inner_kwargs):
            """Wrapper function that checks the return type of the engine function is a WorkflowRun."""
            result = f(*args, **inner_kwargs)
            if not isinstance(result, WorkflowRun):
                raise TypeError(
                    f"Engine '{f.__name__}' must return a WorkflowRun, got: {type(result).__name__}"
                )
            return result

        engine_name = name or f.__name__
        EngineRegistry.register_engine(engine_name, wrapper)
        return wrapper

    if callable(func_or_name):
        return decorator_engine(func_or_name)
    else:
        return decorator_engine

class EngineRegistry:
    """EngineRegistry is a class that contains a registry of engines. 
    It allows for the registration and retrieval of engines by name."""

    engines = {}

    @classmethod
    def register_engine(cls, name, engine : Engine):
        cls.engines[name] = engine

    @classmethod
    def get_engine(cls, name):
        return cls.engines.get(name)

    def __class_getitem__(cls, name):
        if name not in cls.engines:
            raise KeyError(f"Engine'{name}' is not registered. Available engines: {list(cls.engines.keys())}")
        return cls.engines[name]

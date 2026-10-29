from yardstiq.object.engine_registry import EngineRegistry
from typing import Optional

def engine(func: Optional[callable] = None, name: str = None, **kwargs):
    """engine decorator to register an engine in the EngineRegistry. It can be used with or without parameters.
    
    Args:
        func (callable, optional): The function to be decorated. Defaults to None.
        name (str, optional): The name of the engine. Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the engine function.
    """

    def decorator_engine(func: callable):
        """decorator function to register an engine in the EngineRegistry."""

        engine_name = name or func.__name__

        # Register the engine in the EngineRegistry
        EngineRegistry.register_engine(engine_name, func)

        if func is not None:
            return decorator_engine(func)

    return decorator_engine


from functools import wraps
from typing import Callable
from enum import Enum


class Module(Enum):
    HASH = 0
    FUNCTION = 1
    TAGS = 2
    NAME = 3


def module(name: str = None, hash: str = None, tags: list[str] = None):
    """module decorator to register a module in the ModuleRegistry.

    Args:
        name (str): The name of the module.
        hash (str): The hash of the module.
        tags (list[str], optional): A list of tags associated with the module. Defaults to None.
    """
    tags = tags or []
    if hash is None or not isinstance(hash, str):
        raise TypeError(f"Module must provide a hash string.")
    
    def decorator_algorithm(func: Callable):
        module_name = name if name else func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                raise TypeError(f"Module '{func.__name__}' must return a string containing the function as a source code, but returned: {type(result).__name__}") 
            return func(*args, **kwargs)

        ModuleRegistry.register_module(module_name, hash, wrapper, tags=tags)
        return wrapper

    return decorator_algorithm

class ModuleRegistry:
    """ModuleRegistry is a registry that holds all the modules registered in the system."""

    _modules = {}

    @classmethod
    def register_module(cls, name: str, hash: str, func: Callable, tags: list[str] = None):
        """Register a module in the ModuleRegistry."""
        tags = tags or []
        cls._modules[name] = (hash, func, tags, name)

    @classmethod
    def get_module(cls, name: str) -> Callable:
        """Get a module from the ModuleRegistry."""
        if name in cls._modules:
            _, func, _ = cls._modules[name]
            return func

        raise KeyError(f"Module with name '{name}' is not registered.")

    @classmethod
    def get_modules(cls):
        """Get all registered modules."""
        return cls._modules

    @classmethod
    def __class_getitem__(cls, key) -> Callable:
        """Get a module from the ModuleRegistry"""
        if key not in cls._modules:
            raise KeyError(f"Module with name '{key}' is not registered.")  
        return cls._modules[key]

    @classmethod
    def get_modules(cls):
        """Get all registered modules."""
        return cls._modules

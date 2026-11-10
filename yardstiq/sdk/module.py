from functools import wraps
from typing import Callable
from enum import IntEnum, StrEnum
from yardstiq.object import module_database
from yardstiq.object.module import Module


def module(name: str = None, tags: list[str] = None):
    """module decorator to register a module in the ModuleRegistry.

    Args:
        name (str): The name of the module.
        tags (list[str], optional): A list of tags associated with the module. Defaults to None.
    """
    tags = tags or []

    def decorator_module(func: Callable):
        module_name = name if name else func.__name__
        mod = Module(module_name, func)
        module_database.register_module(mod)
        return mod

    return decorator_module

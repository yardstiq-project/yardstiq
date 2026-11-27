import inspect
from typing import Callable

from yardstiq.object.module import Module
from yardstiq.registry import register_module


def module(
    name: str = None,
    tags: list[str] = None,
    local: bool = False,
    qall_args: dict = {},
    version: str = "latest",
):
    """module decorator to register a module in the ModuleRegistry.

    Args:
        name (str): The name of the module.
        tags (list[str], optional): A list of tags associated with the module. Defaults to None.
    """
    tags = tags or []
    qall_args = qall_args or {}

    def decorator_module(func: Callable):
        module_name = name if name else func.__name__
        path = inspect.getsourcefile(func)
        module = Module(
            name=module_name,
            function=func,
            local=local,
            qall_args=qall_args,
            path=path,
            version=version,
            tags=tags,
        )
        register_module(module)
        return module

    return decorator_module

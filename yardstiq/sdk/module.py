from functools import wraps
from typing import Callable

def module(input_type: type = None, output_type: type = None, tag: list[str] = None):
    """module decorator to register a module in the ModuleRegistry.

    Args:
        input_type (type, optional): The type of the input for the module. Defaults to None.
        output_type (type, optional): The type of the output for the module. Defaults to None.
        tag (list[str], optional): A list of tags associated with the module. Defaults to None.
    """
    tag = tag or []

    def decorator_algorithm(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        moduleRegistry.register_module(input_type, output_type, wrapper, tag=tag)
        return wrapper

    return decorator_algorithm


class moduleRegistry:
    """ModuleRegistry is a registry that holds all the modules registered in the system."""

    _modules = []

    @classmethod
    def register_module(cls, input_type: type, output_type: type, func: Callable, tag: list[str] = None):
        """Register a module in the ModuleRegistry."""
        tag = tag or []
        cls._modules.append((input_type, output_type, func, tag))

    @classmethod
    def get_module(cls, input_type: type, output_type: type, tag: list[str] = None) -> Callable:
        """Get a module from the ModuleRegistry."""
        tag = tag or []
        for mod_input_type, mod_output_type, func, mod_tag in cls._modules:
            if mod_input_type == input_type and mod_output_type == output_type and set(mod_tag).issubset(set(tag)):
                return func
                
        in_name = input_type.__name__ if input_type else 'None'
        out_name = output_type.__name__ if output_type else 'None'
        raise KeyError(f"Module with input type '{in_name}', output type '{out_name}', and tags {tag} is not registered.")

    @classmethod
    def __class_getitem__(cls, key) -> Callable:
        """Get a module from the ModuleRegistry using subscript notation (e.g., moduleRegistry[int, str])."""
        if isinstance(key, tuple):
            input_type = key[0]
            output_type = key[1] if len(key) > 1 else None
            tag = key[2] if len(key) > 2 else None
        else:
            input_type = key
            output_type = None
            tag = None
            
        return cls.get_module(input_type, output_type, tag)

    @classmethod
    def get_modules(cls):
        """Get all registered modules."""
        return cls._modules
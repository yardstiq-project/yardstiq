from typing import Callable
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Module:
    """Module is a wrapper for a function. A module is a callable that contains at least preprocess and postprocess methods and an initialization method.
    Each process is dispatch on a specific ressource such as CPU, GPU or QPU
    """

    name: str
    function: Callable
    version: str
    local: bool = False
    path: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    qall_args: dict = field(default_factory=dict)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class ModuleRegistry:
    """ModuleRegistry is a registry that holds all the modules registered in the system."""

    _modules = {}

    def register_module(cls, module: Module):
        """Register a module in the ModuleRegistry."""
        cls._modules[module.name] = module

    def get_module(cls, name: str) -> Callable:
        """Get a module from the ModuleRegistry."""
        if name in cls._modules:
            return cls._modules[name]
        raise KeyError(f"Module with name '{name}' is not registered.")

    def get_modules(cls) -> dict[Module]:
        """Get all registered modules."""
        return cls._modules

    def __getitem__(cls, name) -> Callable:
        """Get a module from the ModuleRegistry"""
        if name not in cls._modules:
            raise KeyError(f"Module with name '{name}' is not registered.")
        return cls._modules[name]

    def get_modules_file(cls, path: str) -> list[Module]:
        return [module for module in cls._modules.values() if module.path == path]

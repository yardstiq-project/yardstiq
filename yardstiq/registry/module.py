from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yardstiq.object import Module


class ModuleRegistry:
    """ModuleRegistry is a registry that holds all the modules registered in the system."""

    _modules = {}

    def register_module(cls, module: Module):
        """Register a module in the ModuleRegistry."""
        cls._modules[module.name] = module

    def get_module(cls, name: str) -> Module:
        """Get a module from the ModuleRegistry."""
        if name in cls._modules:
            return cls._modules[name]
        raise KeyError(f"Module with name '{name}' is not registered.")

    def get_modules(cls) -> dict[Module]:
        """Get all registered modules."""
        return cls._modules

    def __getitem__(cls, name) -> Module:
        """Get a module from the ModuleRegistry"""
        if name not in cls._modules:
            raise KeyError(f"Module with name '{name}' is not registered.")
        return cls._modules[name]

    def get_modules_file(cls, path: str) -> list[Module]:
        return [module for module in cls._modules.values() if module.path == path]

    def get_non_local(cls) -> list[Module]:
        return [module for module in cls._modules.values() if module.local == False]

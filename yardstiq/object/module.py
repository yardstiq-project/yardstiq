from typing import Callable
from dataclasses import dataclass, field
from typing import Optional
from yardstiq.registry import module_database


@dataclass(frozen=True)
class Module:
    """Module is a wrapper for a function. A module is a callable that contains at least preprocess and postprocess methods and an initialization method.
    Each process is dispatch on a specific resource such as CPU, GPU or QPU
    """

    name: str
    function: Callable
    version: str
    local: bool = False
    path: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    qall_args: dict = field(default_factory=dict)
    hash: str = None

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def register(self):
        module_database.register_module(self)

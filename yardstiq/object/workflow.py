
from yardstiq.object.instance import Instance
from yardstiq.object.config import Config
from dataclasses import dataclass

@dataclass(frozen=True)
class Workflow:
    """"""
    instance : Instance
    config : Config
    
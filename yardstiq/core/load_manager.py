from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import Workflow

def load_manager(
        instance : Instance,
        config : Config
) -> Workflow:
    """"""
    return Workflow(instance, config)

    

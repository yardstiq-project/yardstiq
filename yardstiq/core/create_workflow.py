from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import WorkflowInfo
from yardstiq.object.dataset import Dataset

import json

def create_workflow(
        instance : Instance,
        config : Config
) -> WorkflowInfo:
    """Function that loads the dataset and """

    #Check QPU/EMU availability
    #Check dataset availability
    #Check compatibility

    #data = json.load(instance.dataset)
    data = json.load(open(f"{instance.dataset}"))
    dataset = Dataset(name=instance.dataset, hash=data["hash"], version=data["version"], content=data["content"])

    return WorkflowInfo(instance, config, dataset)



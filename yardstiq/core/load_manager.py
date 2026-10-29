from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import WorkflowInfo
from yardstiq.object.dataset import Dataset

import json

def load_manager(
        instance : Instance,
        config : Config
) -> WorkflowInfo:
    """Function that loads the dataset and """

    #Check QPU/EMU availability
    #Check dataset availability
    #Check compatibility

    #data = json.load(instance.dataset)
    data = json.load(open(f"{instance.dataset}"))
    dataset = Dataset(instance.dataset, data)
    return WorkflowInfo(instance, config, dataset)



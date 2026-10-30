from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import Workflow
from yardstiq.object.dataset import Dataset

import json

def create_workflow(
        instance : Instance,
        config : Config
) -> Workflow:
    """Function that loads the dataset and """

    #Check QPU/EMU availability
    #Check dataset availability
    #Check compatibility

    #data = json.load(instance.dataset)
    data = json.load(open(f"{instance.dataset}"))
    dataset = Dataset(instance.dataset, data)
    return Workflow(instance, config, dataset)



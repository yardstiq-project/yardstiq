from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import WorkflowInfo
from yardstiq.object.dataset import Dataset

from pathlib import Path

import json


def create_workflow_info(instance: Instance, config: Config) -> WorkflowInfo:
    """Function that checks availability of the dataset and"""

    # Check QPU/EMU availability
    # Check dataset availability
    # Check compatibility

    # To replace with Aqora API
    file = Path(instance.dataset)
    if not file.is_file():
        raise FileNotFoundError("Dataset file not found")
    #

    return WorkflowInfo(instance, config)

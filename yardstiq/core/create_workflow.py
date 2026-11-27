from yardstiq.object.config import Config
from yardstiq.object.instance import Instance
from yardstiq.object.workflow import WorkflowInfo
from yardstiq.object.dataset import Dataset

from pathlib import Path

import json


def create_workflow_info(
    instance: Instance, config: Config, local: bool = False
) -> WorkflowInfo:
    """Function that checks availability of the dataset and"""

    return WorkflowInfo(instance, config, local)

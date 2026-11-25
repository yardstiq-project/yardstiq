from abc import ABC, abstractmethod
from .workflow import WorkflowRun, WorkflowInfo


class Engine(ABC):
    """"""

    name: str

    @abstractmethod
    def run_workflowinfo(workflow: WorkflowInfo) -> WorkflowRun:
        pass


from yardstiq.object.instance import Instance
from yardstiq.object.config import Config
from yardstiq.object.dataset import Dataset
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowInfo:
    """WorkflowInfo is a combination of an instance, a config and a dataset that can be used to run a problem on a QPU/EMU
    
    Attributes:
        instance : Instance that contains the problem, dataset name and QPU/EMU
        config : Config is a set of parameters that can be used to run the algorithm
        data : Dataset is the data that can be used to run the algorithm
    """
    instance : Instance
    config : Config
    data : Dataset


@dataclass(frozen=True)
class WorkflowRun:
    """WorkflowRun represents a single execution of a workflow
    
    Attributes:
        workflow : WorkflowInfo that contains the Instance, config and data to be used for the execution
        circuit : Circuit that was generated for the execution
        result : Result of the execution
    """
    workflow: WorkflowInfo
    circuit : str
    result : any

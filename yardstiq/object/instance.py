from dataclasses import dataclass
from .config import Config
import typer

PROBLEM_LIST = ["maxcut", ""]

@dataclass(frozen=True)
class Instance:
    """Instance represents the combination of a problem, a dataset and a QPU/EMU

    Attributes:
        Problem : Name of a problem category
        Dataset : Name of a dataset to use
        QPU : Name of a QPU or an emulator
    """
    problem : str
    dataset : str
    qpu : str

    def __init__(self, problem : str, dataset: str, qpu :str):

        if not problem in PROBLEM_LIST:
            raise typer.BadParameter(f"problem {problem} is not supported. List of supported problems : {PROBLEM_LIST} ")
        
        self.problem = problem
        self.dataset = dataset
        self.qpu = qpu


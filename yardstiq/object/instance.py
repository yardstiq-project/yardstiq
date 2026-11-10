from dataclasses import dataclass
from .config import Config
import typer

PROBLEM_LIST = ["maxcut", "tsp", "vqe", "exemple_algorithm"]


@dataclass(frozen=True)
class Instance:
    """Instance represents the combination of a problem, a dataset and a QPU/EMU

    Attributes:
        Problem : Name of a problem category
        Dataset : URI of a dataset to use
        QPU : Name of a QPU or an emulator
    """

    problem: str
    dataset: str

    def __post_init__(self):
        if not self.problem in PROBLEM_LIST:
            raise typer.BadParameter(
                f"problem {self.problem} is not supported. List of supported problems : {PROBLEM_LIST} "
            )

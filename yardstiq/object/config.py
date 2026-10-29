from dataclasses import dataclass, field, fields
import warnings
import typer

@dataclass(frozen=True)
class Config:
    """Config represents the hyper parameters of an algorithm

    Attributes:
        max_shot: Maximum shot over QPU/EMU
        max_duration: Maximum duration of execution on QPU/EMU
        max_cost: Maximum cost of execution on QPU/EMU
        max_iteration : ?
        max_depth : Maximum depth of a circuit
        compilation_parameters : Other parameters needed for compilation
    """

    max_shot: int = 10000
    max_duration: int = 10000
    max_cost: int = 200
    max_iteration: int = 3
    max_depth: int = 10
    compilation_parameters: dict = field(default_factory=dict)

    @classmethod
    def from_dict(self, data : dict):
        """Creates a config from a dict and ignore non used parameters"""

        valid = {key.name for key in fields(self)}
        print(data)
        filtered = {}
        for raw_key, val in data.items():
            key = raw_key.replace('-', '_')

            if key in valid:
                if key != "compilation_parameters":
                    try:
                        filtered[key] = int(val)
                    except ValueError:
                        raise typer.BadParameter(f"Config parameter {key} must be an integer, got {val}")
                else: 
                    # This part needs further discussions
                    filtered[key] = val
            else:
                warnings.warn(f"Passed config parameter is not supported: {key}")
        return self(**filtered)


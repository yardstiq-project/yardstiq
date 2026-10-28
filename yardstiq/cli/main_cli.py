import typer
from typing import Optional
from yardstiq.object.instance import Instance
from yardstiq.core.load_manager import load_manager
from .utils import config_parser

PROBLEM_LIST = ["maxcut", ""]

app = typer.Typer(
    name="ys",
    help="A python tool for quantum benchmark",
    no_args_is_help=True
)

@app.command("run")
def run(
    problem: str = typer.Argument(
        ..., help="Name of a problem category to be run by the benchmark"
    ),
    dataset: str = typer.Argument(
        ..., help="Name of a dataset to use with the problem"
    ),
    qpu: str = typer.Argument(
        ..., help="Name of a QPU or emulator to run benchmark"
    ),
    config: Optional[str] = typer.Option(
        None, "--config", "-c", help="Config option for execution"
    ),
    ):
    """Take a specific problem with a dataset and a QPU/EMU to run an instance.
        E.g.: ys maxcut aqora-maxcut-01 qiskit-aer -c 'max-shot 10000 max-duration 10000 ...' """
    typer.echo(f"Initiating compilation run for: {problem}, {dataset}, {qpu}")

    parsed_instance = Instance(problem, dataset, qpu)

    parsed_config = config_parser(config)
    typer.echo(f"Config used : {parsed_config}" if config else f"Using default config : {parsed_config}")

    workflow = load_manager(parsed_instance, parsed_config)

    



    


@app.command("estimate")
def estimate():
    print(f"Not implemented yet")


@app.command("tool")
def tool():
    print(f"Not implemented yet")


@app.command("login")
def login():
    print(f"Not implemented yet")

@app.command("logout")
def logout():
    print(f"Not implemented yet")



import typer
from typing import Optional
from yardstiq.object.instance import Instance
from yardstiq.core.create_workflow import create_workflow
from yardstiq.core.create_workflowrun import create_workflowrun
from .utils import create_config, debug_print
from .tool import tool_cli


app = typer.Typer(
    name="ys",
    help="A python tool for quantum benchmark",
    no_args_is_help=True
)

app.add_typer(tool_cli)


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
    estimate: Optional[bool] = typer.Option(
        False, "--estimate", "-e", help="Option to prevent from running problem and estimate ressources cost"
    ),
    pipeline: Optional[str] = typer.Option(
        "qall", "--pipeline", "-p", help="Option so declare which pipeline to use when running workflow"
    ),
    debug: Optional[bool] = typer.Option(
        False, "--debug", help="Option to print log info"
    )
    ):
    """Take a specific problem with a dataset and a QPU/EMU to run an instance.
        E.g.: ys run maxcut aqora-maxcut-01 qiskit-aer -c 'max-shot 10000 max-duration 10000 ...' """

    debug_print(f"Initiating compilation run for: {problem}, {dataset}, {qpu}", debug)

    parsed_instance = Instance(problem, dataset, qpu)
    debug_print(f"Instance parsed: {parsed_instance}", debug)

    parsed_config = create_config(config)
    debug_print(f"Config used : {parsed_config}" if config else f"Using default config : {parsed_config}", True)

    workflow = create_workflow(parsed_instance, parsed_config)
    debug_print(f"Workflow created : {workflow}", debug)

    workflow_run = create_workflowrun(workflow, pipeline)
    debug_print(f"Workflowrun executed : {workflow_run}", debug)

    #submission manager part

@app.command("login")
def login():
    print(f"Not implemented yet")

@app.command("logout")
def logout():
    print(f"Not implemented yet")

import typer
from yardstiq.core.data_base import register_algo, register_module
from yardstiq.object import algorithm_database


algo_cli = typer.Typer(
    name="algo", help="Yardstiq's algorithm CLI", no_args_is_help=True
)


@algo_cli.command("add")
def algo(
    problem: str = typer.Argument(
        ..., help="Name of the problem to import"
    ),
    path: str = typer.Argument(
        ..., help="Path to the file containing the problem"
    ),
    req: list[str] = typer.Option(
        [], "--requirement", "-r", help="Depedencies needed to execute module(s)"
    ),
):
    """Import algorithms to YS"""
    register_algo(path, problem, req)

@algo_cli.command("ls")
def list_algo():
    """List all algorithms registered in Yardstiq"""
    lst = algorithm_database.get_algorithms()
    typer.echo(f"List of algorithms registered:")
    for algo in lst.values():
        typer.echo(f"Algorithm : name= {algo.problem}, hash= {algo.hash}")
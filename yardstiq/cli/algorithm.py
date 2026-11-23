import typer
from yardstiq.core.data_base import register_algo, clear_algo
from yardstiq.object import algorithm_database
from yardstiq.object.algorithm import Algorithm

algo_cli = typer.Typer(
    name="algo", help="Yardstiq's algorithm CLI", no_args_is_help=True
)


@algo_cli.command("add")
def algo(
    problem: str = typer.Argument(..., help="Name of the problem to import"),
    path: str = typer.Argument(..., help="Path to the file containing the problem"),
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
    for problem, algos in lst.items():
        typer.echo(f"Algorithm type : {problem}")
        for algo in algos:
            typer.echo(f"Algorithm : {algo.name}")

@algo_cli.command("clear")
def clear_algos():
    """Clear all algorithms registered in Yardstiq"""
    clear_algo()


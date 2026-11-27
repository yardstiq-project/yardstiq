import typer

from yardstiq.database.data_base import register_algo, clear_algo, delete_algo
from .utils import load_file, get_import_algorithm
from yardstiq.registry import algorithm_database
from yardstiq.registry.push_qall import push_algorithm_qall

algo_cli = typer.Typer(
    name="algorithm", help="Yardstiq's algorithm CLI", no_args_is_help=True
)


@algo_cli.command("add")
def algorithm_add(
    problem: str = typer.Argument(..., help="Name of the problem to import"),
    path: str = typer.Argument(..., help="Path to the file containing the problem"),
    requirement: list[str] = typer.Option(
        [], "--requirement", "-r", help="Depedencies needed to execute module(s)"
    ),
):
    """Import algorithms to YS"""
    try:
        folder = load_file(path)
    except Exception as e:
        return typer.echo(f"Error : {e}")

    algorithm = get_import_algorithm(problem)
    if not algorithm:
        return typer.echo(f"Error: No algorithms found under problem {problem}")

    hash = push_algorithm_qall(folder, algorithm, requirement)
    register_algo(algorithm, hash)


@algo_cli.command("ls")
def list_algo():
    """List all algorithms registered in Yardstiq"""
    lst = algorithm_database.get_algorithms()
    typer.echo("List of algorithms registered:")
    for problem, algorithms in lst.items():
        typer.echo(f"\nAlgorithm type : {problem}")
        typer.echo(f"{'ID':<18} {'NAME':<34} {'HASH'}")
        for algorithm in algorithms:
            typer.echo(f"{str(algorithm.id):<18} {algorithm.name:<34} {algorithm.hash}")


@algo_cli.command("clear")
def clear_algos():
    """Clear all algorithms registered in Yardstiq"""
    clear_algo()


@algo_cli.command("delete")
def clear_algos(
    id: str = typer.Argument(..., help="Name of the algorithm to delete"),
):
    """Clear specific algorithm registered in Yardstiq"""
    if not delete_algo(id):
        typer.echo(f"Warning: can't delete algorithm with id : {id}")
    else:
        typer.echo(f"Successfully removed algorithm : {id}")

import typer
from yardstiq.database.data_base import register_module, clear_module
from yardstiq.object import module_database
from yardstiq.database.data_base import cursor
from yardstiq.modules import load_db
from yardstiq.object.module import Module

module_cli = typer.Typer(
    name="module", help="Yardstiq's modules CLI", no_args_is_help=True
)


@module_cli.command("add")
def module(
    path: str = typer.Argument(..., help="Path to the file containing the module(s)"),
    req: list[str] = typer.Option(
        [], "--requirement", "-r", help="Depedencies needed to execute module(s)"
    ),
):
    """Add a module to YS"""
    register_module(path, req)


@module_cli.command("ls")
def list_module():
    """List all modules registered in Yardstiq"""

    lst = module_database.get_modules()
    typer.echo(f"List of modules registered:")
    for module in lst.values():
        typer.echo(
            f"Module : name= {module.name}, hash= {module.hash}, tags= {module.tags}"
        )


@module_cli.command("clear")
def clear_modules():
    """Clear all modules registered in Yardstiq"""
    clear_module()

import typer
from yardstiq.registry import module_database

from .utils import load_file, get_import_modules
from yardstiq.registry.push_qall import push_module_qall

from yardstiq.database.data_base import register_module, clear_module

module_cli = typer.Typer(
    name="module", help="Yardstiq's modules CLI", no_args_is_help=True
)


@module_cli.command("add")
def module(
    path: str = typer.Argument(..., help="Path to the file containing the module(s)"),
    requirement: list[str] = typer.Option(
        [], "--requirement", "-r", help="Depedencies needed to execute module(s)"
    ),
):
    """Add a module to YS"""
    try:
        folder = load_file(path)
    except Exception as e:
        return typer.echo(f"Error : {e}")

    modules = get_import_modules()
    if not modules or len(modules) == 0:
        return typer.echo(f"Error: No modules found in file {path}")

    for module in modules:
        hash = push_module_qall(folder, module, requirement)
        register_module(module, hash)


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

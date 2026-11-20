import typer
from yardstiq.core.ressources import print_ressoures
from typing import Optional


tool_cli = typer.Typer(
    name="tool", help="Tools for Yardstiq", no_args_is_help=True
)


@tool_cli.command("ressource")
def list_ressources(
    local: Optional[bool] = typer.Option(
    False, "--local", help="Option to run the workflow remotely on a server"
    ),
):
    """Prints all ressources available"""
    print_ressoures(local)
    

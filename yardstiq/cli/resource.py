import typer
from yardstiq.core.ressources import print_resources
from typing import Optional

resource_cli = typer.Typer(name="resource", help="Resources for Yardstiq", no_args_is_help=True)


@resource_cli.command("ls")
def list_resources(
    local: Optional[bool] = typer.Option(
        False, "--local", help="Option to run the workflow remotely on a server"
    ),
):
    """Prints all ressources available"""
    print_resources(local)

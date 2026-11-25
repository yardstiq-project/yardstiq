import typer
from yardstiq.core.resources import list_provider_resources
from typing import Optional
from .utils import list_ressource_str

resource_cli = typer.Typer(
    name="resource", help="Resources for Yardstiq", no_args_is_help=True
)


@resource_cli.command("ls")
def list_resources(
    local: Optional[bool] = typer.Option(
        False, "--local", help="Option to run the workflow remotely on a server"
    ),
):
    """Prints all resources available"""

    lst = list_provider_resources(local)
    lst_str = list_ressource_str(lst)
    typer.echo(lst_str)

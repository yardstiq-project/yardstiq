import typer

from qall.object.resource import ResourceAvailability, Resource
from qall.provider.workflow import get_provider_client_by_name
from qall.provider.workflow.provider_client import WorkflowProviderClient
from qall.provider.login import get_provider_login_credentials, get_logged_provider_name
from qall.provider.workflow.local import get_local_qpu_resources


def log_to_provider() -> WorkflowProviderClient | None:
    """Log to provider using stored data"""
    name = get_logged_provider_name()
    creds = get_provider_login_credentials()

    if creds == None or name == None:
        return None

    provider = get_provider_client_by_name(name)
    provider.login(creds.credentials)
    return provider


def list_provider_resources(local: bool = False) -> None | str:
    """Prints all resources available from provider"""

    provider = log_to_provider()
    if not local:
        if provider is None:
            typer.echo("Can't connect to provider")
            return
        lst = provider.list_resources()
    else:
        lst = get_local_qpu_resources()

    return lst

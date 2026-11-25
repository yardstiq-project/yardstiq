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


PROVIDER = log_to_provider()


def check_hardware_availability(
    hardware: str,
    ressources: list[Resource],
    filter: dict | None = None,
) -> Resource | None:
    res = [elem for elem in ressources if elem.name == hardware]

    s = len(res)
    if s == 0:
        typer.echo("Error: no hardware found in provider resources")
        return None
    elif s > 1:
        typer.echo(
            "Error: multiple hardwares found in provider resources. Please adjust filters"
        )
        return None
    return res[0]


def print_resources(local: bool = False):
    """Prints all resources available from provider"""

    if not local:
        if PROVIDER is None:
            typer.echo("Can't connect to provider")
            return
        lst = PROVIDER.list_resources()
    else:
        lst = get_local_qpu_resources()

    typer.echo("Resources List")
    typer.echo(f"{'NAME':<30} {'AVAILABILITY':<15} {'PROVIDER NAME':<16} {'TYPE':<12} {'MODALITY':<16} {'TOPOLOGY':<15}")

    for resource in lst:
        if resource.availability == ResourceAvailability.available:
            avail = resource.availability.value
            prov = str(resource.provider)
            
            if resource.qpu:
                qpu_type = resource.qpu.type.value
                modality = resource.qpu.modality.value
                topology = resource.qpu.topology.value
            else:
                qpu_type = modality = topology = "N/A"

            typer.echo(f"{resource.name:<30} {avail:<15} {prov:<16} {qpu_type:<12} {modality:<16} {topology:<15}")

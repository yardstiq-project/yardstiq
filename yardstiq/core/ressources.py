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
        print("Error: no hardware found in provider resources")
        return None
    elif s > 1:
        print(
            "Error: multiple hardwares found in provider resources. Please adjust filters"
        )
        return None
    return res[0]


def print_ressoures(local: bool = False):
    """Prints all ressources available from provider"""

    if not local:
        if PROVIDER == None:
            print("Can't connect to provider")
            return
        lst = PROVIDER.list_resources()
    else:
        lst = get_local_qpu_resources()

    for ressource in lst:
        if ressource.availability == ResourceAvailability.available:
            print(ressource.name)
            print(ressource.availability)
            print(ressource.provider)
            print(ressource.price)
            print(ressource.qpu)
            print("\n")

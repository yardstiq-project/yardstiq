import typer
from yardstiq.object.config import Config
from typing import Optional
from qall.object.resource import Resource, ResourceAvailability


def create_config(raw: Optional[str], qpu: str) -> Config:
    """Function to parse config text into Config structure"""
    if raw == None:
        return Config(hardware=qpu)

    lst = raw.split()
    if len(lst) % 2 != 0:
        raise typer.BadParameter("missing a key or a value in config")

    parsed_config = {}

    for i in range(0, len(lst) - 1, 2):
        if i + 1 < len(lst):
            key = lst[i]
            value = lst[i + 1]
            parsed_config[key] = value
    parsed_config["hardware"] = qpu
    return Config.from_dict(parsed_config)


def debug_print(msg: str, debug: bool):
    """Function to print debug message if debug is True"""
    if debug:
        typer.echo(msg)


def parse_extra_args(args: list[str]) -> dict[str, str]:
    """
    Parses arbitrary extra CLI option flags into a clean Python dictionary.
    Handles '--key=value', '--key value', and standalone boolean flags.
    Normalizes keys by removing leading dashes and replacing hyphens with underscores.

    Example:
        ['--project-id=123', '--secret-key', 'abc', '--verbose']
        -> {'project_id': '123', 'secret_key': 'abc', 'verbose': 'true'}
    """
    extra_dict = {}
    i = 0

    while i < len(args):
        arg = args[i]

        if arg.startswith("--"):
            # Clean the prefix and prepare the key
            clean_arg = arg.lstrip("-")

            if "=" in clean_arg:
                # Case A: Syntax option is '--key=value'
                key, val = clean_arg.split("=", 1)
                extra_dict[key.replace("-", "_")] = val
                i += 1
            else:
                # Case B: Syntax option is '--key value' or standalone flag
                key = clean_arg.replace("-", "_")

                # Check if the next argument exists and is a value (not another flag)
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    extra_dict[key] = args[i + 1]
                    i += 2
                else:
                    # Fallback flag default value if standalone
                    extra_dict[key] = "true"
                    i += 1
        else:
            # Skip invalid positions or unformatted extra strings
            i += 1

    return extra_dict


def list_ressource_str(lst: list[Resource]) -> str:
    lst_str = f"{'NAME':<30} {'AVAILABILITY':<15} {'PROVIDER NAME':<16} {'TYPE':<12} {'MODALITY':<16} {'TOPOLOGY':<15}"

    lst = sorted(lst, key=lambda r: r.qpu.type.value if r.qpu else "")

    for resource in lst:
        if resource.availability == ResourceAvailability.available:
            avail = resource.availability.value
            prov = str(resource.provider)

            if resource.qpu:
                qpu_type = resource.qpu.type.value
                modality = resource.qpu.modality.value
                topology = resource.qpu.topology.name
            else:
                qpu_type = modality = topology = "N/A"

            lst_str += f"{resource.name:<30} {avail:<15} {prov:<16} {qpu_type:<12} {modality:<16} {topology:<15}"
    return lst_str

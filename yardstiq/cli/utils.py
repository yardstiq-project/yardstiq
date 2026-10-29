import typer
from yardstiq.object.config import Config
from typing import Optional


def config_parser(raw : Optional[str]) -> Config:
    """Function to parse config text into Config structure"""
    if not raw:
        return Config()
    
    lst = raw.split()
    if len(lst) % 2 != 0:
        raise typer.BadParameter("missing a key or a value in config")

    parsed_config = {}

    for i in range(0, len(lst) - 1, 2):
        if i + 1 < len(lst):
            key = lst[i]
            value = lst[i + 1]
            parsed_config[key] = value
    
    return Config.from_dict(parsed_config)


def debug_print(msg : str, debug : bool):
    """Function to print debug message if debug is True"""
    if debug:
        typer.echo(msg)

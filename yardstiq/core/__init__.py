from .ressources import log_to_provider, PROVIDER
import typer

if PROVIDER == None:
    typer.echo("Warning: No provider found")
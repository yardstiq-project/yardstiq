from .ressources import PROVIDER
import typer

if PROVIDER == None:
    typer.echo("Warning: No provider found")

import typer
import qall

from yardstiq.core.provider import login_provider_ys, logout_provider_ys
from .utils import parse_extra_args
from typing import Optional

provider_cli = typer.Typer(
    name="provider",
    help="Configure compute provider environments",
    no_args_is_help=True,
)


@provider_cli.command(
    "login", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def login(
    ctx: typer.Context,  # Typer Context is mandatory to capture extra unkown arguments
    provider_name: str = typer.Argument(
        ...,
        help="Name of the cloud provider (e.g., scaleway, braket, qbraid, azure...).",
    ),
    registry_domain: Optional[str] = typer.Option(
        None,
        "--registry",
        "-r",
        help="Domain URI of the content-addressed registry server.",
    ),
):
    """
    Authenticate against a provider and optionally a Qall registry.
    Examples:
        ys provider login scaleway --project-id=XYZ --secret-key=ABC
        or
        ys provider login scaleway
        This will prompt for the required credentials interactively.
    """
    creds = parse_extra_args(ctx.args)

    try:
        client = qall.core.get_provider_client_by_name(provider_name)
    except Exception as e:
        typer.echo(f"Error : {e}", err=True)
        raise typer.Exit(code=1)

    fields = client.get_credential_fields()

    if fields and len(fields) > 0:
        for field in fields:
            key_name = field["name"]

            if key_name not in creds or not creds[key_name]:
                creds[key_name] = typer.prompt(
                    field["prompt"],
                    hide_input=field.get("hide_input", False),
                )

    if not creds:
        typer.echo(
            "Warning: No credentials flags passed (e.g. --api-key=XYZ).",
            err=True,
        )

    try:
        if qall.core.login_provider(provider_name=provider_name, credentials=creds):
            qall.core.init_config(
                provider_name=provider_name,
                erase_exists=False,
                generate_default_config=True,
            )
        typer.echo(f" Successfully authenticated on {provider_name}.")
    except Exception as e:
        typer.echo(f" Failed to login to {provider_name} : {e}", err=True)
        raise typer.Exit(code=1)

    if registry_domain:
        try:
            qall.core.login_registry(registry_domain=registry_domain, credentials=creds)
            typer.echo(f" Successfully authenticated on {registry_domain}.")
        except Exception as e:
            typer.echo(f" Failed to login to {registry_domain} : {e}", err=True)
            raise typer.Exit(code=1)


@provider_cli.command("logout")
def logout():
    old_provider = logout_provider_ys()

    if old_provider:
        typer.echo(f"Dropped provider credentials successfully from {old_provider}")
    else:
        typer.echo(f"Already logout")

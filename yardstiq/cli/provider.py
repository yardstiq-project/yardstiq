import typer
from yardstiq.core.provider import login_provider_ys, logout_provider_ys

provider_cli = typer.Typer(
    name="provider", help="Configure compute provider environments", no_args_is_help=True
)

@provider_cli.command(
    "login", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def provider_login(
    ctx: typer.Context,
    provider_name: str = typer.Argument(
        ..., help="Compute provider identity token identifier (e.g., scaleway)."
    ),
):
    """Authenticate the local instance against a provider control plane."""
    creds = parse_extra_args(ctx.args)

    if not creds:
        typer.echo(
            "Warning: No credentials flags passed (e.g. --api-key=XYZ).",
            err=True,
        )

    try:
        login_provider_ys(provider_name=provider_name, credentials=creds)
        typer.echo(f" Successfully authenticated on {provider_name}.")
    except Exception as e:
        typer.echo(f" Failed to login to {provider_name} : {e}", err=True)
        raise typer.Exit(code=1)

@provider_cli.command("logout")
def provider_logout():
    old_provider = logout_provider_ys()

    if old_provider:
        typer.echo(f"Dropped provider credentials successfully from {old_provider}")
    else:
        typer.echo(f"Already logout")


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

import typer

tool_cli = typer.Typer(
    name="tool",
    help="Generate tools for Yardstiq",
    no_args_is_help=True
)

@tool_cli.command("generate")
def generate():
    """Generate resources for Yardstiq. This command is not yet implemented."""
    raise typer.BadParameter("generate is not yet implemented")


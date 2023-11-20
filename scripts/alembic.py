import subprocess
from pathlib import Path
from typing import Annotated

import typer

BASE_ARGS_KEY = "base_args"
SQL_OPT = "--sql"
DEFAULT_PATH = Path(__file__).parent.parent / "migrations" / "alembic.ini"
BASE_ARGS = ["alembic", "--config"]

state = {BASE_ARGS_KEY: BASE_ARGS}


cli_app = typer.Typer(add_completion=False, no_args_is_help=True)


@cli_app.callback()
def callback(
    config_file: Annotated[
        Path,
        typer.Option(..., "-c", "--config", exists=True, help="Config file to use."),
    ] = DEFAULT_PATH,
) -> None:
    """Database migration tool."""
    state[BASE_ARGS_KEY] = BASE_ARGS + [str(config_file)]


@cli_app.command()
def migrate(
    message: Annotated[
        str, typer.Option(..., "-m", "--message", help="Message for the migration.")
    ],
) -> None:
    """Auto-generate a migration file for the database."""
    args = state[BASE_ARGS_KEY] + ["revision", "--autogenerate", "-m", message]
    subprocess.run(args)


@cli_app.command()
def upgrade(
    revision: Annotated[str, typer.Argument(help="Revision to upgrade to.")] = "head",
    sql: Annotated[
        bool,
        typer.Option(
            help="Show SQL statements generated by the upgrade process.",
        ),
    ] = False,
) -> None:
    """Upgrade the database."""
    args = state[BASE_ARGS_KEY] + ["upgrade", revision]
    if sql:
        args.append(SQL_OPT)
    subprocess.run(args)


@cli_app.command()
def downgrade(
    revision: Annotated[str, typer.Argument(help="Revision to downgrade to.")] = "-1",
    sql: Annotated[
        bool,
        typer.Option(
            help="Show SQL statements generated by the upgrade process.",
        ),
    ] = False,
) -> None:
    """Downgrade the database."""
    if sql and revision == "-1":
        revision = "head:-1"
    args = state[BASE_ARGS_KEY] + ["downgrade", revision]
    if sql:
        args.append(SQL_OPT)
    subprocess.run(args)


@cli_app.command()
def stamp(
    revision: Annotated[
        str, typer.Argument(help="Revision to stamp as current revision.")
    ] = "head",
) -> None:
    """Stamp the database."""
    args = state[BASE_ARGS_KEY] + ["stamp", revision]
    subprocess.run(args)


@cli_app.command()
def current() -> None:
    """Show the current revision."""
    args = state[BASE_ARGS_KEY] + ["current"]
    subprocess.run(args)


if __name__ == "__main__":
    cli_app()
"""Defines the entry point for the `blctl` command-line interface.

The root Click group registers subcommands from `blctl.commands`.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.commands import engage


@click.group()
@click.version_option(package_name="breachlock-blctl")
def cli() -> None:
    """Provides the `blctl` command-line interface for BreachLock AEV."""


cli.add_command(engage)


def main() -> None:
    """Runs the `blctl` CLI."""
    cli()


if __name__ == "__main__":
    main()

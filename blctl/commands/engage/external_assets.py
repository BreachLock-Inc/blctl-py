"""Defines external asset registration for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.api.client import ApiClient
from blctl.api.models import ExternalAssetItem
from blctl.commands.engage.cli_errors import call_or_exit


def register_external_assets(
    *,
    client: ApiClient,
    organization_id: str,
    targets: list[str],
) -> list[str]:
    """Registers targets as manually added external assets.

    Args:
        `client` (`ApiClient`): The API client to use.
        `organization_id` (`str`): The organization under which to register.
        `targets` (`list[str]`): IPs or hostnames to register.
    Returns:
        `list[str]`: Newly created asset IDs, or an empty list when `targets`
            is empty.
    """
    if not targets:
        return []
    click.echo(
        f"Registering {len(targets)} target(s) as external assets...",
        err=True,
    )
    registered = call_or_exit(
        lambda: client.create_external_assets(
            [
                ExternalAssetItem(
                    organization_id=organization_id,
                    hostname=target,
                )
                for target in targets
            ]
        )
    )
    return [entry.asset_id for entry in registered]

"""Defines network engagement launch flows for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.api.client import ApiClient
from blctl.api.models import (
    EngagementCreated,
    ExternalNetworkEngagementRequest,
    InternalNetworkEngagementRequest,
)
from blctl.commands.engage.cli_errors import call_or_exit
from blctl.commands.engage.common_engagement_fields import CommonEngagementFields
from blctl.commands.engage.external_assets import register_external_assets
from blctl.commands.engage.network_recon_fields import NetworkReconFields


def start_external_network_engagement(
    *,
    client: ApiClient,
    organization_id: str,
    targets: list[str],
    preexisting_asset_ids: list[str],
    common_fields: CommonEngagementFields,
    network_recon_fields: NetworkReconFields,
) -> EngagementCreated:
    """Registers targets and starts an external network engagement.

    Args:
        `client` (`ApiClient`): The API client to use.
        `organization_id` (`str`): The organization under which to run.
        `targets` (`list[str]`): IPs or hostnames to register first.
        `preexisting_asset_ids` (`list[str]`): Asset IDs from `--asset-id`.
        `common_fields` (`CommonEngagementFields`): Shared engagement fields.
        `network_recon_fields` (`NetworkReconFields`): Network recon toggles.
    Returns:
        `EngagementCreated`: The created engagement summary.
    """
    registered_asset_ids = register_external_assets(
        client=client,
        organization_id=organization_id,
        targets=targets,
    )
    combined_asset_ids = [*registered_asset_ids, *preexisting_asset_ids]
    request = ExternalNetworkEngagementRequest(
        organization_id=organization_id,
        asset_ids=combined_asset_ids,
        **common_fields.model_dump(exclude={"asset_ids"}),
        **network_recon_fields.model_dump(),
    )
    click.echo(
        f"Starting external network engagement `{request.name}` against "
        f"{len(request.asset_ids)} asset(s)...",
        err=True,
    )
    return call_or_exit(lambda: client.create_external_network_engagement(request))


def start_internal_network_engagement(
    *,
    client: ApiClient,
    deployment_id: str,
    azure_ad_recon: bool,
    common_fields: CommonEngagementFields,
    network_recon_fields: NetworkReconFields,
) -> EngagementCreated:
    """Starts an internal network engagement on an existing deployment.

    Args:
        `client` (`ApiClient`): The API client to use.
        `deployment_id` (`str`): The deployment to run on.
        `azure_ad_recon` (`bool`): Whether to run Azure AD reconnaissance.
        `common_fields` (`CommonEngagementFields`): Shared engagement fields.
        `network_recon_fields` (`NetworkReconFields`): Network recon toggles.
    Returns:
        `EngagementCreated`: The created engagement summary.
    """
    request = InternalNetworkEngagementRequest(
        deployment_id=deployment_id,
        is_azure_active_directory_reconnaissance=azure_ad_recon,
        **common_fields.model_dump(),
        **network_recon_fields.model_dump(),
    )
    click.echo(
        f"Starting internal network engagement `{request.name}` on deployment "
        f"{deployment_id} against {len(request.asset_ids)} asset(s)...",
        err=True,
    )
    return call_or_exit(lambda: client.create_internal_network_engagement(request))

"""Defines web engagement launch flows for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.api.client import ApiClient
from blctl.api.models import (
    EngagementCreated,
    ExternalWebEngagementRequest,
    InternalWebEngagementRequest,
    WebEngagementCredentials,
)
from blctl.commands.engage.cli_errors import call_or_exit
from blctl.commands.engage.common_engagement_fields import CommonEngagementFields
from blctl.commands.engage.external_assets import register_external_assets


def start_external_web_engagement(
    *,
    client: ApiClient,
    organization_id: str,
    targets: list[str],
    preexisting_asset_ids: list[str],
    credentials: WebEngagementCredentials | None,
    common_fields: CommonEngagementFields,
) -> EngagementCreated:
    """Registers targets and starts an external web engagement.

    Args:
        `client` (`ApiClient`): The API client to use.
        `organization_id` (`str`): The organization under which to run.
        `targets` (`list[str]`): IPs or hostnames to register first.
        `preexisting_asset_ids` (`list[str]`): Asset IDs from `--asset-id`.
        `credentials` (`WebEngagementCredentials | None`): Optional login creds.
        `common_fields` (`CommonEngagementFields`): Shared engagement fields.
    Returns:
        `EngagementCreated`: The created engagement summary.
    """
    registered_asset_ids = register_external_assets(
        client=client,
        organization_id=organization_id,
        targets=targets,
    )
    combined_asset_ids = [*registered_asset_ids, *preexisting_asset_ids]
    request = ExternalWebEngagementRequest(
        organization_id=organization_id,
        credentials=credentials,
        asset_ids=combined_asset_ids,
        **common_fields.model_dump(exclude={"asset_ids"}),
    )
    credential_suffix = " with credentials" if credentials else " (unauthenticated)"
    click.echo(
        f"Starting external web engagement `{request.name}` against "
        f"{len(request.asset_ids)} asset(s){credential_suffix}...",
        err=True,
    )
    return call_or_exit(lambda: client.create_external_web_engagement(request))


def start_internal_web_engagement(
    *,
    client: ApiClient,
    deployment_id: str,
    credentials: WebEngagementCredentials | None,
    common_fields: CommonEngagementFields,
) -> EngagementCreated:
    """Starts an internal web engagement on an existing deployment.

    Args:
        `client` (`ApiClient`): The API client to use.
        `deployment_id` (`str`): The deployment to run on.
        `credentials` (`WebEngagementCredentials | None`): Optional login creds.
        `common_fields` (`CommonEngagementFields`): Shared engagement fields.
    Returns:
        `EngagementCreated`: The created engagement summary.
    """
    request = InternalWebEngagementRequest(
        deployment_id=deployment_id,
        credentials=credentials,
        **common_fields.model_dump(),
    )
    credential_suffix = " with credentials" if credentials else " (unauthenticated)"
    click.echo(
        f"Starting internal web engagement `{request.name}` on deployment "
        f"{deployment_id} against {len(request.asset_ids)} asset(s)"
        f"{credential_suffix}...",
        err=True,
    )
    return call_or_exit(lambda: client.create_internal_web_engagement(request))

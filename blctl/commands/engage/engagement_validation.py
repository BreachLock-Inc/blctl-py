"""Defines CLI validation for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.commands.engage.parsing import split_comma_separated


def validate_engagement_flags(
    *,
    engagement_type: str,
    is_external: bool,
    is_internal: bool,
    targets_csv: str | None,
    asset_ids: tuple[str, ...],
    organization_id: str | None,
    deployment_id: str | None,
    advanced_network_recon: bool,
    advanced_web_server_recon: bool,
    active_directory_recon: bool,
    azure_ad_recon: bool,
    web_username: str | None,
    web_password: str | None,
    web_totp_secret: str | None,
) -> list[str]:
    """Validates engagement CLI flags before any API call is made.

    Args:
        `engagement_type` (`str`): The `--type` value.
        `is_external` (`bool`): Whether `--external` was passed.
        `is_internal` (`bool`): Whether `--internal` was passed.
        `targets_csv` (`str | None`): The raw `--targets` value.
        `asset_ids` (`tuple[str, ...]`): Asset IDs from `--asset-id`.
        `organization_id` (`str | None`): The `--organization-id` value.
        `deployment_id` (`str | None`): The `--deployment-id` value.
        `advanced_network_recon` (`bool`): Advanced network recon flag.
        `advanced_web_server_recon` (`bool`): Advanced web server recon flag.
        `active_directory_recon` (`bool`): Active Directory recon flag.
        `azure_ad_recon` (`bool`): Azure AD recon flag.
        `web_username` (`str | None`): The `--username` value.
        `web_password` (`str | None`): The `--password` value.
        `web_totp_secret` (`str | None`): The `--totp-secret` value.
    Returns:
        `list[str]`: Parsed target hostnames/IPs for external engagements.
    Raises:
        `click.UsageError`: When flags are missing or mutually incompatible.
    """
    normalised_type = engagement_type.lower()
    is_web = normalised_type == "web"

    if is_external and is_internal:
        raise click.UsageError("--external and --internal are mutually exclusive.")

    if not (is_external or is_internal):
        raise click.UsageError(
            f"For --type={normalised_type}, you must specify either "
            "--external or --internal."
        )

    targets = split_comma_separated(targets_csv)
    if is_external:
        if not organization_id:
            raise click.UsageError(
                "--organization-id (or env BLCTL_ORGANIZATION_ID) is required "
                "for --external."
            )
        if deployment_id is not None:
            raise click.UsageError(
                "--deployment-id is not valid for --external; the portal "
                "creates an ephemeral deployment for each external engagement."
            )
        if azure_ad_recon:
            raise click.UsageError(
                "--azure-ad-recon is only valid with --type=network --internal."
            )
        if not targets and not asset_ids:
            raise click.UsageError(
                "At least one of --targets or --asset-id is required for " "--external."
            )
    else:
        if deployment_id is None:
            raise click.UsageError("--deployment-id is required for --internal.")
        if targets_csv is not None:
            raise click.UsageError(
                "--targets is not supported for --internal. Internal assets "
                "come from a prior ping sweep on the deployment; pass their "
                "CUIDs via --asset-id."
            )
        if not asset_ids:
            raise click.UsageError(
                "--asset-id is required for --internal (at least one)."
            )

    if is_web:
        if advanced_network_recon:
            raise click.UsageError(
                "--advanced-network-recon is only valid for --type=network."
            )
        if advanced_web_server_recon:
            raise click.UsageError(
                "--advanced-web-server-recon is only valid for --type=network."
            )
        if active_directory_recon:
            raise click.UsageError(
                "--active-directory-recon is only valid for --type=network."
            )
        if azure_ad_recon:
            raise click.UsageError(
                "--azure-ad-recon is only valid for --type=network --internal."
            )
        if (web_username is None) != (web_password is None):
            raise click.UsageError(
                "--username and --password must be supplied together (or "
                "neither, for an unauthenticated scan)."
            )
        if web_totp_secret is not None and web_username is None:
            raise click.UsageError("--totp-secret requires --username and --password.")
    elif (
        web_username is not None
        or web_password is not None
        or web_totp_secret is not None
    ):
        raise click.UsageError(
            "--username, --password, and --totp-secret are only valid "
            "for --type=web."
        )

    return targets


def resolve_type_default_flags(
    *,
    is_web: bool,
    exploitation: bool | None,
    learn_findings: bool | None,
    learn_exploits: bool | None,
) -> tuple[bool, bool, bool]:
    """Resolves per-type defaults for exploitation and learning flags.

    Args:
        `is_web` (`bool`): Whether the engagement type is web.
        `exploitation` (`bool | None`): The explicit `--exploitation` value.
        `learn_findings` (`bool | None`): The explicit `--learn-findings` value.
        `learn_exploits` (`bool | None`): The explicit `--learn-exploits` value.
    Returns:
        `tuple[bool, bool, bool]`: Resolved `(exploitation, learn_findings,
            learn_exploits)` values.
    """
    type_default = is_web
    resolved_exploitation = exploitation if exploitation is not None else type_default
    resolved_learn_findings = (
        learn_findings if learn_findings is not None else type_default
    )
    resolved_learn_exploits = (
        learn_exploits if learn_exploits is not None else type_default
    )
    return resolved_exploitation, resolved_learn_findings, resolved_learn_exploits

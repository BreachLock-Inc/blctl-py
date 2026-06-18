"""Defines the `engage` Click command for starting pentest engagements.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.api.client import ApiClient
from blctl.api.enums import (
    SCAN_INTENSITY_CHOICES,
    SCORE_SEVERITY_CHOICES,
    VULNERABILITY_CONFIDENCE_CHOICES,
    ScanIntensity,
    ScoreSeverity,
    VulnerabilityConfidence,
)
from blctl.commands.engage.engagement_validation import (
    resolve_type_default_flags,
    validate_engagement_flags,
)
from blctl.commands.engage.field_builders import (
    build_common_engagement_fields,
    build_network_recon_fields,
    build_web_engagement_credentials,
)
from blctl.commands.engage.network_engagements import (
    start_external_network_engagement,
    start_internal_network_engagement,
)
from blctl.commands.engage.parsing import parse_notify_url
from blctl.commands.engage.web_engagements import (
    start_external_web_engagement,
    start_internal_web_engagement,
)


@click.command("engage")
@click.option(
    "--type",
    "engagement_type",
    type=click.Choice(["network", "web"], case_sensitive=False),
    required=True,
    help="Engagement type. `network` runs a network pentest; `web` runs a web "
    "application pentest (which accepts optional agentic login credentials).",
)
@click.option(
    "--external",
    "is_external",
    is_flag=True,
    help="Run the engagement against externally reachable targets.",
)
@click.option(
    "--internal",
    "is_internal",
    is_flag=True,
    help="Run the engagement against internal targets via a deployed agent.",
)
@click.option(
    "--targets",
    "targets_csv",
    type=str,
    default=None,
    help=(
        "Comma-separated list of IPs or hostnames to scan (external only). "
        "Each target is registered as a manually added external asset before "
        "the engagement is started. Not valid for --internal."
    ),
)
@click.option(
    "--asset-id",
    "asset_ids",
    type=str,
    multiple=True,
    help=(
        "Asset ID (CUID) to include in the engagement. Repeatable. For "
        "--external these are external asset IDs (combinable with --targets); "
        "for --internal these are internal asset IDs from a prior ping sweep "
        "on the chosen deployment (at least one required)."
    ),
)
@click.option(
    "--organization-id",
    type=str,
    default=None,
    envvar="BLCTL_ORGANIZATION_ID",
    help=(
        "Organization ID (CUID). Required for --external; ignored for "
        "--internal (the deployment determines the organization). "
        "Defaults to $BLCTL_ORGANIZATION_ID."
    ),
)
@click.option(
    "--deployment-id",
    type=str,
    default=None,
    help=(
        "Deployment ID (CUID). Required for --internal; not valid for "
        "--external (the portal creates an ephemeral deployment automatically)."
    ),
)
@click.option(
    "--name",
    "engagement_name",
    type=str,
    required=True,
    help="Human-readable name for the engagement.",
)
@click.option(
    "--api-key",
    type=str,
    required=True,
    envvar="BLCTL_API_KEY",
    help="BreachLock API key (Bearer token). Defaults to $BLCTL_API_KEY.",
)
@click.option(
    "--api-url",
    type=str,
    required=True,
    envvar="BLCTL_API_URL",
    help=(
        "Base URL of your BreachLock AEV tenant "
        "(e.g. https://tenant.app.breachlock.com). Defaults to $BLCTL_API_URL."
    ),
)
@click.option(
    "--severity-threshold",
    type=click.Choice(SCORE_SEVERITY_CHOICES, case_sensitive=False),
    default=ScoreSeverity.NONE.value,
    show_default=True,
    help="Minimum severity threshold for results.",
)
@click.option(
    "--confidence-threshold",
    type=click.Choice(VULNERABILITY_CONFIDENCE_CHOICES, case_sensitive=False),
    default=VulnerabilityConfidence.VERY_LOW.value,
    show_default=True,
    help="Minimum confidence threshold for vulnerabilities.",
)
@click.option(
    "--scan-intensity",
    type=click.Choice(SCAN_INTENSITY_CHOICES, case_sensitive=False),
    default=ScanIntensity.NORMAL.value,
    show_default=True,
    help="Scan intensity (affects host timeout and depth).",
)
@click.option(
    "--advanced-network-recon/--no-advanced-network-recon",
    default=False,
    help="Run advanced network reconnaissance. Network engagements only.",
)
@click.option(
    "--advanced-web-server-recon/--no-advanced-web-server-recon",
    default=False,
    help="Run advanced web server reconnaissance. Network engagements only.",
)
@click.option(
    "--active-directory-recon/--no-active-directory-recon",
    default=False,
    help="Run Active Directory reconnaissance. Network engagements only.",
)
@click.option(
    "--azure-ad-recon/--no-azure-ad-recon",
    default=False,
    help="Run Azure AD reconnaissance. Only valid with --type=network --internal.",
)
@click.option(
    "--credential-recovery/--no-credential-recovery",
    default=False,
    help="Attempt credential recovery.",
)
@click.option(
    "--tailored-remediation/--no-tailored-remediation",
    default=False,
    help="Provide tailored remediation advice.",
)
@click.option(
    "--screenshots/--no-screenshots",
    default=False,
    help="Capture screenshots.",
)
@click.option(
    "--exploitation/--no-exploitation",
    default=None,
    help=(
        "Attempt exploitation. Defaults to false for --type=network and true "
        "for --type=web (matching the portal's per-type defaults)."
    ),
)
@click.option(
    "--learn-findings/--no-learn-findings",
    default=None,
    help=(
        "Feed findings back into the BreachLock learning pipeline. Defaults "
        "to false for --type=network and true for --type=web."
    ),
)
@click.option(
    "--learn-exploits/--no-learn-exploits",
    default=None,
    help=(
        "Feed exploits back into the BreachLock learning pipeline. Defaults "
        "to false for --type=network and true for --type=web."
    ),
)
@click.option(
    "--username",
    "web_username",
    type=str,
    default=None,
    envvar="BLCTL_WEB_USERNAME",
    help=(
        "Username the engagement agent should use to log in to the target "
        "web application. Only valid for --type=web. Must be paired with "
        "--password. Defaults to $BLCTL_WEB_USERNAME."
    ),
)
@click.option(
    "--password",
    "web_password",
    type=str,
    default=None,
    envvar="BLCTL_WEB_PASSWORD",
    help=(
        "Password the engagement agent should use to log in to the target "
        "web application. Only valid for --type=web. Must be paired with "
        "--username. Prefer $BLCTL_WEB_PASSWORD to keep the secret out of "
        "shell history and CI logs."
    ),
)
@click.option(
    "--totp-secret",
    "web_totp_secret",
    type=str,
    default=None,
    envvar="BLCTL_WEB_TOTP_SECRET",
    help=(
        "Base32 TOTP shared secret for multi-factor authentication. Only "
        "valid for --type=web together with --username/--password. Prefer "
        "$BLCTL_WEB_TOTP_SECRET."
    ),
)
@click.option(
    "--excluded-protocol",
    "excluded_protocols",
    type=str,
    multiple=True,
    help="Protocol ID or code to exclude from the engagement. Repeatable.",
)
@click.option(
    "--excluded-finding",
    "excluded_findings",
    type=str,
    multiple=True,
    help="Finding ID or code to exclude from the engagement. Repeatable.",
)
@click.option(
    "--excluded-cve",
    "excluded_cves",
    type=str,
    multiple=True,
    help="CVE to exclude from the engagement. Repeatable.",
)
@click.option(
    "--included-cve",
    "included_cves",
    type=str,
    multiple=True,
    help="CVE to explicitly include in the engagement. Repeatable.",
)
@click.option(
    "--notify-url",
    "notify_url_specifications",
    type=str,
    multiple=True,
    help=(
        "Webhook URL to notify on engagement updates. Repeatable. Pass either a "
        "bare URL (`https://hook/`) or a URL with pipe-separated `Name=Value` "
        "headers (`https://hook/|Authorization=Bearer abc|X-Trace=42`)."
    ),
)
@click.option(
    "--shield-slug",
    "shield_slug",
    type=str,
    default=None,
    help=(
        "CI/CD shield slug for this engagement. When set, the engagement's "
        "results can be displayed via the shield badge at "
        "/api/public/v1/shield/{shieldSlug}."
    ),
)
@click.option(
    "--threat-actor-assessment-id",
    "threat_actor_assessment_ids",
    type=str,
    multiple=True,
    help=(
        "Threat actor assessment ID (CUID) to associate with the engagement. "
        "Repeatable."
    ),
)
def engage(
    engagement_type: str,
    is_external: bool,
    is_internal: bool,
    targets_csv: str | None,
    asset_ids: tuple[str, ...],
    organization_id: str | None,
    deployment_id: str | None,
    engagement_name: str,
    api_key: str,
    api_url: str,
    severity_threshold: str,
    confidence_threshold: str,
    scan_intensity: str,
    advanced_network_recon: bool,
    advanced_web_server_recon: bool,
    active_directory_recon: bool,
    azure_ad_recon: bool,
    credential_recovery: bool,
    tailored_remediation: bool,
    screenshots: bool,
    exploitation: bool | None,
    learn_findings: bool | None,
    learn_exploits: bool | None,
    web_username: str | None,
    web_password: str | None,
    web_totp_secret: str | None,
    excluded_protocols: tuple[str, ...],
    excluded_findings: tuple[str, ...],
    excluded_cves: tuple[str, ...],
    included_cves: tuple[str, ...],
    notify_url_specifications: tuple[str, ...],
    threat_actor_assessment_ids: tuple[str, ...],
    shield_slug: str | None,
) -> None:
    """Starts a pentest engagement against BreachLock AEV."""
    is_web = engagement_type.lower() == "web"
    targets = validate_engagement_flags(
        engagement_type=engagement_type,
        is_external=is_external,
        is_internal=is_internal,
        targets_csv=targets_csv,
        asset_ids=asset_ids,
        organization_id=organization_id,
        deployment_id=deployment_id,
        advanced_network_recon=advanced_network_recon,
        advanced_web_server_recon=advanced_web_server_recon,
        active_directory_recon=active_directory_recon,
        azure_ad_recon=azure_ad_recon,
        web_username=web_username,
        web_password=web_password,
        web_totp_secret=web_totp_secret,
    )
    resolved_exploitation, resolved_learn_findings, resolved_learn_exploits = (
        resolve_type_default_flags(
            is_web=is_web,
            exploitation=exploitation,
            learn_findings=learn_findings,
            learn_exploits=learn_exploits,
        )
    )
    notify_urls = [
        parse_notify_url(specification) for specification in notify_url_specifications
    ]
    common_fields = build_common_engagement_fields(
        engagement_name=engagement_name,
        asset_ids=list(asset_ids),
        severity_threshold=severity_threshold,
        confidence_threshold=confidence_threshold,
        scan_intensity=scan_intensity,
        credential_recovery=credential_recovery,
        tailored_remediation=tailored_remediation,
        screenshots=screenshots,
        exploitation=resolved_exploitation,
        learn_findings=resolved_learn_findings,
        learn_exploits=resolved_learn_exploits,
        excluded_protocols=list(excluded_protocols),
        excluded_findings=list(excluded_findings),
        excluded_cves=list(excluded_cves),
        included_cves=list(included_cves),
        notify_urls=notify_urls,
        threat_actor_assessment_ids=list(threat_actor_assessment_ids),
        shield_slug=shield_slug,
    )

    with ApiClient(base_url=api_url, api_key=api_key) as client:
        if is_web:
            credentials = build_web_engagement_credentials(
                username=web_username,
                password=web_password,
                totp_secret=web_totp_secret,
            )
            if is_external:
                assert organization_id is not None
                result = start_external_web_engagement(
                    client=client,
                    organization_id=organization_id,
                    targets=targets,
                    preexisting_asset_ids=list(asset_ids),
                    credentials=credentials,
                    common_fields=common_fields,
                )
            else:
                assert deployment_id is not None
                result = start_internal_web_engagement(
                    client=client,
                    deployment_id=deployment_id,
                    credentials=credentials,
                    common_fields=common_fields,
                )
        else:
            network_recon_fields = build_network_recon_fields(
                advanced_network_recon=advanced_network_recon,
                advanced_web_server_recon=advanced_web_server_recon,
                active_directory_recon=active_directory_recon,
            )
            if is_external:
                assert organization_id is not None
                result = start_external_network_engagement(
                    client=client,
                    organization_id=organization_id,
                    targets=targets,
                    preexisting_asset_ids=list(asset_ids),
                    common_fields=common_fields,
                    network_recon_fields=network_recon_fields,
                )
            else:
                assert deployment_id is not None
                result = start_internal_network_engagement(
                    client=client,
                    deployment_id=deployment_id,
                    azure_ad_recon=azure_ad_recon,
                    common_fields=common_fields,
                    network_recon_fields=network_recon_fields,
                )

    click.echo(result.model_dump_json(by_alias=True, indent=2))

"""Defines engagement field builders for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.enums import ScanIntensity, ScoreSeverity, VulnerabilityConfidence
from blctl.api.models import NotifyUrl, WebEngagementCredentials
from blctl.commands.engage.common_engagement_fields import CommonEngagementFields
from blctl.commands.engage.network_recon_fields import NetworkReconFields


def build_common_engagement_fields(
    *,
    engagement_name: str,
    asset_ids: list[str],
    severity_threshold: str,
    confidence_threshold: str,
    scan_intensity: str,
    credential_recovery: bool,
    tailored_remediation: bool,
    screenshots: bool,
    exploitation: bool,
    learn_findings: bool,
    learn_exploits: bool,
    excluded_protocols: list[str],
    excluded_findings: list[str],
    excluded_cves: list[str],
    included_cves: list[str],
    notify_urls: list[NotifyUrl],
    threat_actor_assessment_ids: list[str],
    shield_slug: str | None,
) -> CommonEngagementFields:
    """Bundles shared engagement fields into a `CommonEngagementFields` model.

    Args:
        `engagement_name` (`str`): The human-readable engagement name.
        `asset_ids` (`list[str]`): Asset IDs to include in the engagement.
        `severity_threshold` (`str`): The severity threshold CLI value.
        `confidence_threshold` (`str`): The confidence threshold CLI value.
        `scan_intensity` (`str`): The scan intensity CLI value.
        `credential_recovery` (`bool`): Whether to attempt credential recovery.
        `tailored_remediation` (`bool`): Whether to provide tailored remediation.
        `screenshots` (`bool`): Whether to capture screenshots.
        `exploitation` (`bool`): Whether to attempt exploitation.
        `learn_findings` (`bool`): Whether to feed findings into learning.
        `learn_exploits` (`bool`): Whether to feed exploits into learning.
        `excluded_protocols` (`list[str]`): Protocols to exclude.
        `excluded_findings` (`list[str]`): Findings to exclude.
        `excluded_cves` (`list[str]`): CVEs to exclude.
        `included_cves` (`list[str]`): CVEs to include.
        `notify_urls` (`list[NotifyUrl]`): Webhook targets.
        `threat_actor_assessment_ids` (`list[str]`): Threat actor assessment IDs.
        `shield_slug` (`str | None`): Optional CI/CD shield slug for badge rendering.
    Returns:
        `CommonEngagementFields`: The bundled common engagement fields.
    """
    return CommonEngagementFields(
        name=engagement_name,
        asset_ids=asset_ids,
        severity_threshold=ScoreSeverity(severity_threshold.upper()),
        confidence_threshold=VulnerabilityConfidence(confidence_threshold.upper()),
        scan_intensity=ScanIntensity(scan_intensity.upper()),
        attempt_credential_recovery=credential_recovery,
        provide_tailored_remediation_advice=tailored_remediation,
        capture_screenshots=screenshots,
        attempt_exploitation=exploitation,
        learn_findings=learn_findings,
        learn_exploits=learn_exploits,
        excluded_protocols=excluded_protocols,
        excluded_findings=excluded_findings,
        excluded_cves=excluded_cves,
        included_cves=included_cves,
        notify_urls=notify_urls,
        threat_actor_assessment_ids=threat_actor_assessment_ids,
        shield_slug=shield_slug,
    )


def build_network_recon_fields(
    *,
    advanced_network_recon: bool,
    advanced_web_server_recon: bool,
    active_directory_recon: bool,
) -> NetworkReconFields:
    """Bundles network-only recon toggles into a `NetworkReconFields` model.

    Args:
        `advanced_network_recon` (`bool`): Advanced network recon flag.
        `advanced_web_server_recon` (`bool`): Advanced web server recon flag.
        `active_directory_recon` (`bool`): Active Directory recon flag.
    Returns:
        `NetworkReconFields`: The bundled network recon fields.
    """
    return NetworkReconFields(
        run_advanced_network_reconnaissance=advanced_network_recon,
        run_advanced_web_server_reconnaissance=advanced_web_server_recon,
        run_active_directory_reconnaissance=active_directory_recon,
    )


def build_web_engagement_credentials(
    *,
    username: str | None,
    password: str | None,
    totp_secret: str | None,
) -> WebEngagementCredentials | None:
    """Assembles web engagement credentials from CLI options.

    All-or-nothing on username and password is enforced before this is called.

    Args:
        `username` (`str | None`): The web application username.
        `password` (`str | None`): The web application password.
        `totp_secret` (`str | None`): The optional TOTP shared secret.
    Returns:
        `WebEngagementCredentials | None`: Credentials for an authenticated scan,
            or `None` for an unauthenticated scan.
    """
    if username is None and password is None:
        return None
    assert username is not None
    assert password is not None
    return WebEngagementCredentials(
        username=username,
        password=password,
        totp_secret=totp_secret,
    )

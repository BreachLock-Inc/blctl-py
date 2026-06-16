"""Defines the `EngagementRequestBase` model shared by all engagement requests.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import Field

from blctl.api.enums import ScanIntensity, ScoreSeverity, VulnerabilityConfidence
from blctl.api.models.notify_url import NotifyUrl
from blctl.api.models.request_model import RequestModel


class EngagementRequestBase(RequestModel):
    """Represents fields shared by every engagement creation request.

    Not intended to be instantiated directly; subclasses layer on type-specific
    fields (network recon toggles, web credentials, etc.) and direction-specific
    fields (`organization_id` for external, `deployment_id` for internal).
    """

    name: str
    """The human-readable engagement name."""

    asset_ids: list[str]
    """The asset IDs (CUIDs) to include in the engagement."""

    severity_threshold: ScoreSeverity = ScoreSeverity.NONE
    """The minimum severity threshold for results."""

    confidence_threshold: VulnerabilityConfidence = VulnerabilityConfidence.VERY_LOW
    """The minimum confidence threshold for vulnerabilities."""

    attempt_credential_recovery: bool = False
    """Whether to attempt credential recovery during the engagement."""

    provide_tailored_remediation_advice: bool = False
    """Whether to provide tailored remediation advice in findings."""

    capture_screenshots: bool = False
    """Whether to capture screenshots during the engagement."""

    attempt_exploitation: bool = False
    """Whether to attempt exploitation of discovered vulnerabilities."""

    learn_findings: bool = False
    """Whether to feed findings back into the BreachLock learning pipeline."""

    learn_exploits: bool = False
    """Whether to feed exploits back into the BreachLock learning pipeline."""

    excluded_protocols: list[str] = Field(default_factory=list)
    """Protocol IDs or codes to exclude from the engagement."""

    excluded_findings: list[str] = Field(default_factory=list)
    """Finding IDs or codes to exclude from the engagement."""

    excluded_cves: list[str] = Field(default_factory=list)
    """CVE IDs to exclude from the engagement."""

    included_cves: list[str] = Field(default_factory=list)
    """CVE IDs to explicitly include in the engagement."""

    notify_urls: list[NotifyUrl] = Field(default_factory=list)
    """Webhook targets for engagement status updates."""

    scan_intensity: ScanIntensity = ScanIntensity.NORMAL
    """The scan intensity (affects host timeout and depth)."""

    threat_actor_assessment_ids: list[str] = Field(default_factory=list)
    """Threat actor assessment IDs (CUIDs) to associate with the engagement."""

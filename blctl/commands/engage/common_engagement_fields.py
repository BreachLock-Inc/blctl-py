"""Defines `CommonEngagementFields` for shared engagement request fields.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import BaseModel, Field

from blctl.api.enums import ScanIntensity, ScoreSeverity, VulnerabilityConfidence
from blctl.api.models import NotifyUrl


class CommonEngagementFields(BaseModel):
    """Represents fields shared by every engagement creation request."""

    name: str
    """The human-readable engagement name."""

    asset_ids: list[str]
    """The asset IDs (CUIDs) to include in the engagement."""

    severity_threshold: ScoreSeverity
    """The minimum severity threshold for results."""

    confidence_threshold: VulnerabilityConfidence
    """The minimum confidence threshold for vulnerabilities."""

    scan_intensity: ScanIntensity
    """The scan intensity (affects host timeout and depth)."""

    attempt_credential_recovery: bool
    """Whether to attempt credential recovery."""

    provide_tailored_remediation_advice: bool
    """Whether to provide tailored remediation advice."""

    capture_screenshots: bool
    """Whether to capture screenshots."""

    attempt_exploitation: bool
    """Whether to attempt exploitation."""

    learn_findings: bool
    """Whether to feed findings back into the learning pipeline."""

    learn_exploits: bool
    """Whether to feed exploits back into the learning pipeline."""

    excluded_protocols: list[str] = Field(default_factory=list)
    """Protocol IDs or codes to exclude."""

    excluded_findings: list[str] = Field(default_factory=list)
    """Finding IDs or codes to exclude."""

    excluded_cves: list[str] = Field(default_factory=list)
    """CVE IDs to exclude."""

    included_cves: list[str] = Field(default_factory=list)
    """CVE IDs to explicitly include."""

    notify_urls: list[NotifyUrl] = Field(default_factory=list)
    """Webhook targets for engagement updates."""

    threat_actor_assessment_ids: list[str] = Field(default_factory=list)
    """Threat actor assessment IDs to associate with the engagement."""

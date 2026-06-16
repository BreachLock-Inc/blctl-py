"""Defines the `WebEngagementRequestBase` model for web engagements.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.engagement_request_base import EngagementRequestBase
from blctl.api.models.web_engagement_credentials import WebEngagementCredentials


class WebEngagementRequestBase(EngagementRequestBase):
    """Represents fields shared by internal and external web engagement requests.

    Web engagements do not expose network recon toggles (the portal hard-codes
    them to `false`). They accept optional agentic login credentials. Defaults
    for `attempt_exploitation`, `learn_findings`, and `learn_exploits` are
    `True` here, matching the portal's web-specific Zod defaults.
    """

    attempt_exploitation: bool = True
    """Whether to attempt exploitation of discovered vulnerabilities."""

    learn_findings: bool = True
    """Whether to feed findings back into the BreachLock learning pipeline."""

    learn_exploits: bool = True
    """Whether to feed exploits back into the BreachLock learning pipeline."""

    credentials: WebEngagementCredentials | None = None
    """Optional credentials the engagement agent uses to log in to the target."""

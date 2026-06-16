"""Defines the `WebEngagementCredentials` model for agentic web login.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.request_model import RequestModel


class WebEngagementCredentials(RequestModel):
    """Represents authentication credentials for agentic web application login.

    Pass `None` at the request-model level for an unauthenticated scan.
    Supplying credentials results in `AgenticCredential` rows persisted against
    the engagement and each of its assets server-side.
    """

    username: str
    """The username used to authenticate to the target web application."""

    password: str
    """The password used to authenticate to the target web application."""

    totp_secret: str | None = None
    """The Base32 TOTP shared secret for multi-factor authentication, if any."""

"""Defines the `WebhookHeader` model for webhook delivery headers.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.request_model import RequestModel


class WebhookHeader(RequestModel):
    """Represents a single HTTP header attached to a webhook delivery."""

    name: str
    """The HTTP header name."""

    value: str
    """The HTTP header value."""

"""Defines the `NotifyUrl` model for engagement webhook targets.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import Field

from blctl.api.models.request_model import RequestModel
from blctl.api.models.webhook_header import WebhookHeader


class NotifyUrl(RequestModel):
    """Represents a webhook target (URL plus optional custom headers)."""

    url: str
    """The webhook URL to notify when engagement updates occur."""

    headers: list[WebhookHeader] = Field(default_factory=list)
    """Optional HTTP headers included on each POST to this URL."""

"""Defines the `ExternalWebEngagementRequest` model.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.web_engagement_request_base import WebEngagementRequestBase


class ExternalWebEngagementRequest(WebEngagementRequestBase):
    """Represents the request body for `POST /api/public/v1/engagement/web/external`.

    The portal creates a fresh ephemeral deployment for each external web
    engagement. `asset_ids` must reference external assets in scope for the
    organization (e.g. previously registered via `POST /api/public/v1/external-asset`).
    """

    organization_id: str
    """The organization ID (CUID) under which to run the engagement."""

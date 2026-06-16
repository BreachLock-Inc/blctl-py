"""Defines the `InternalWebEngagementRequest` model.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.web_engagement_request_base import WebEngagementRequestBase


class InternalWebEngagementRequest(WebEngagementRequestBase):
    """Represents the request body for `POST /api/public/v1/engagement/web/internal`.

    Internal web engagements run via an existing deployment (which must be in
    `READY` state) and target internal assets previously discovered via a ping
    sweep against that deployment.
    """

    deployment_id: str
    """The deployment ID (CUID) on which to run the engagement."""

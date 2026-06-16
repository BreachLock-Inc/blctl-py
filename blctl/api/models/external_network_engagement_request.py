"""Defines the `ExternalNetworkEngagementRequest` model.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.network_engagement_request_base import (
    NetworkEngagementRequestBase,
)


class ExternalNetworkEngagementRequest(NetworkEngagementRequestBase):
    """Represents the request body for `POST /api/public/v1/engagement/network/external`.

    The portal creates a fresh ephemeral deployment for each external network
    engagement, so this request supplies the `organization_id` rather than
    binding to a pre-existing deployment.
    """

    organization_id: str
    """The organization ID (CUID) under which to run the engagement."""

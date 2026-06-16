"""Defines the `InternalNetworkEngagementRequest` model.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.network_engagement_request_base import (
    NetworkEngagementRequestBase,
)


class InternalNetworkEngagementRequest(NetworkEngagementRequestBase):
    """Represents the request body for `POST /api/public/v1/engagement/network/internal`.

    Internal engagements run via an existing deployment (which must be in
    `READY` state) and target internal assets the agent has previously
    discovered via a ping sweep. The organization is inferred from the
    deployment, so this request has no `organization_id` field.
    """

    deployment_id: str
    """The deployment ID (CUID) on which to run the engagement."""

    is_azure_active_directory_reconnaissance: bool = False
    """Whether to run Azure Active Directory reconnaissance."""

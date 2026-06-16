"""Defines the `EngagementCreated` model for engagement creation responses.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.response_model import ResponseModel


class EngagementCreated(ResponseModel):
    """Represents the response body returned when an engagement is created.

    All engagement creation endpoints (network external/internal, web
    external/internal) share this minimal shape.
    """

    id: str
    """The engagement ID (CUID)."""

    name: str
    """The engagement name."""

    deployment_id: str
    """The deployment ID (CUID) running the engagement."""

    deployment_command_id: str
    """The deployment command ID (CUID) for the enqueued engage command."""

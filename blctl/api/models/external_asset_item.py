"""Defines the `ExternalAssetItem` model for the external-asset batch endpoint.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.request_model import RequestModel


class ExternalAssetItem(RequestModel):
    """Represents one entry in the `POST /api/public/v1/external-asset` batch."""

    organization_id: str
    """The organization ID (CUID) under which to register the asset."""

    hostname: str
    """The hostname or IP address to register as a manually added external asset."""

"""Defines the `ExternalAssetResult` model for external-asset registration responses.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from typing import Literal

from blctl.api.models.response_model import ResponseModel


class ExternalAssetResult(ResponseModel):
    """Represents one entry in the `POST /api/public/v1/external-asset` response."""

    asset_id: str
    """The asset ID (CUID) assigned to the registered target."""

    external_asset_id: str
    """The external asset ID (CUID) for the registration."""

    domain_report_id: str
    """The domain report ID (CUID) created or updated for this asset."""

    domain_investigation_id: str
    """The domain investigation ID (CUID) scoped to the organization."""

    hostname: str
    """The hostname that was registered."""

    ip_address: str
    """The resolved IP address for the hostname."""

    status: Literal["created", "updated"]
    """Whether the asset was newly created or updated in place."""

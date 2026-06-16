"""Defines the `NetworkEngagementRequestBase` model for network engagements.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.engagement_request_base import EngagementRequestBase


class NetworkEngagementRequestBase(EngagementRequestBase):
    """Represents fields shared by internal and external network engagement requests.

    Adds the network-only recon toggles on top of the shared engagement base;
    direction-specific subclasses then add `organization_id` (external) or
    `deployment_id` plus `is_azure_active_directory_reconnaissance` (internal).
    """

    run_advanced_network_reconnaissance: bool = False
    """Whether to run advanced network reconnaissance."""

    run_advanced_web_server_reconnaissance: bool = False
    """Whether to run advanced web server reconnaissance."""

    run_active_directory_reconnaissance: bool = False
    """Whether to run Active Directory reconnaissance."""

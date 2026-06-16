"""Defines `NetworkReconFields` for network-only engagement recon toggles.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import BaseModel


class NetworkReconFields(BaseModel):
    """Represents network-only reconnaissance toggles for network engagements."""

    run_advanced_network_reconnaissance: bool
    """Whether to run advanced network reconnaissance."""

    run_advanced_web_server_reconnaissance: bool
    """Whether to run advanced web server reconnaissance."""

    run_active_directory_reconnaissance: bool
    """Whether to run Active Directory reconnaissance."""

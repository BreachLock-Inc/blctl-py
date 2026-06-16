"""Defines the `ScanIntensity` enumeration for engagement scan depth.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from enum import StrEnum


class ScanIntensity(StrEnum):
    """An enumeration of scan intensity levels accepted by the public API."""

    STEALTH = "STEALTH"
    """Represents the stealthiest scan intensity."""

    QUIET = "QUIET"
    """Represents a quiet scan intensity."""

    POLITE = "POLITE"
    """Represents a polite scan intensity."""

    NORMAL = "NORMAL"
    """Represents the default scan intensity."""

    AGGRESSIVE = "AGGRESSIVE"
    """Represents an aggressive scan intensity."""

    EXTREME = "EXTREME"
    """Represents the most aggressive scan intensity."""


SCAN_INTENSITY_CHOICES: list[str] = [member.value for member in ScanIntensity]
"""Valid `--scan-intensity` values for Click option choices."""

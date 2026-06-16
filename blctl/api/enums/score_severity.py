"""Defines the `ScoreSeverity` enumeration for engagement severity thresholds.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from enum import StrEnum


class ScoreSeverity(StrEnum):
    """An enumeration of severity thresholds accepted by the public API."""

    NONE = "NONE"
    """Represents no minimum severity threshold."""

    LOW = "LOW"
    """Represents a low severity threshold."""

    MEDIUM = "MEDIUM"
    """Represents a medium severity threshold."""

    HIGH = "HIGH"
    """Represents a high severity threshold."""

    CRITICAL = "CRITICAL"
    """Represents a critical severity threshold."""


SCORE_SEVERITY_CHOICES: list[str] = [member.value for member in ScoreSeverity]
"""Valid `--severity-threshold` values for Click option choices."""

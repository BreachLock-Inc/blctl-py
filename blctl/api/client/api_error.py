"""Defines the `ApiError` exception for public API error responses.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import json


class ApiError(Exception):
    """Represents an error returned by the BreachLock AEV public API."""

    def __init__(
        self,
        status_code: int,
        message: str,
        details: object | None = None,
    ) -> None:
        """Initializes a new `ApiError`.

        Args:
            `status_code` (`int`): The HTTP status code returned by the portal.
            `message` (`str`): The human-readable error message.
            `details` (`object | None`): Optional structured error details from
                the response body (e.g. Zod validation errors).
        """
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Returns a human-readable representation of this error.

        Returns:
            `str`: The error message, HTTP status, and optional details.
        """
        if self.details:
            return (
                f"{self.message} (HTTP {self.status_code}): "
                f"{json.dumps(self.details, default=str)}"
            )
        return f"{self.message} (HTTP {self.status_code})"

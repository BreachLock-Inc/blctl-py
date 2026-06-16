"""Defines the `ApiErrorBody` model for non-2xx public API responses.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from blctl.api.models.response_model import ResponseModel


class ApiErrorBody(ResponseModel):
    """Represents a parsed non-2xx response body from the BreachLock public API."""

    message: str | None = None
    """The human-readable error message, when present."""

    errors: object | None = None
    """The Zod `flatten()` validation errors object, when the failure was a 400."""

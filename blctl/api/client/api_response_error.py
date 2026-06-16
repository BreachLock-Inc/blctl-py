"""Defines the `ApiResponseError` exception for unexpected 2xx response shapes.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import ValidationError


class ApiResponseError(Exception):
    """Represents a 2xx response body that does not match the expected schema.

    This indicates either API contract drift on the server or a bug in the
    client's models; it should not happen during normal operation.
    """

    def __init__(self, endpoint: str, validation_error: ValidationError) -> None:
        """Initializes a new `ApiResponseError`.

        Args:
            `endpoint` (`str`): The API path that returned the unexpected body.
            `validation_error` (`ValidationError`): The Pydantic validation
                failure describing the schema mismatch.
        """
        super().__init__(str(validation_error))
        self.endpoint = endpoint
        self.validation_error = validation_error

    def __str__(self) -> str:
        """Returns a human-readable representation of this error.

        Returns:
            `str`: The endpoint and validation failure details.
        """
        return (
            f"Unexpected response shape from {self.endpoint}: "
            f"{self.validation_error}"
        )

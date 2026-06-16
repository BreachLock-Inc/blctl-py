"""Defines the `ApiClient` HTTP client for the BreachLock public v1 API.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from __future__ import annotations

from types import TracebackType
from typing import TypeVar

import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError

from blctl.api.client.api_error import ApiError
from blctl.api.client.api_response_error import ApiResponseError
from blctl.api.models import (
    ApiErrorBody,
    EngagementCreated,
    ExternalAssetItem,
    ExternalAssetResult,
    ExternalNetworkEngagementRequest,
    ExternalWebEngagementRequest,
    InternalNetworkEngagementRequest,
    InternalWebEngagementRequest,
)

ResponseModelT = TypeVar("ResponseModelT", bound=BaseModel)
"""Type variable for Pydantic response models validated by `ApiClient`."""

_EXTERNAL_ASSET_LIST_ADAPTER: TypeAdapter[list[ExternalAssetResult]] = TypeAdapter(
    list[ExternalAssetResult]
)
"""Validates the list response from `POST /api/public/v1/external-asset`."""


class ApiClient:
    """Represents a client for the BreachLock AEV public v1 API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout: float = 60.0,
    ) -> None:
        """Initializes a new `ApiClient`.

        Args:
            `base_url` (`str`): The portal base URL (e.g.
                `https://tenant.app.breachlock.com`).
            `api_key` (`str`): The Bearer API key for authentication.
            `timeout` (`float`): The HTTP request timeout in seconds.
        """
        normalised_base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=normalised_base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    def __enter__(self) -> ApiClient:
        """Enters the client context manager.

        Returns:
            `ApiClient`: This client instance.
        """
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exits the client context manager and closes the underlying HTTP client."""
        self.close()

    def close(self) -> None:
        """Closes the underlying HTTP client and releases connections."""
        self._client.close()

    def create_external_assets(
        self,
        items: list[ExternalAssetItem],
    ) -> list[ExternalAssetResult]:
        """Registers manually added external assets in batch.

        Args:
            `items` (`list[ExternalAssetItem]`): Each item must contain
                `organization_id` and `hostname`.
        Returns:
            `list[ExternalAssetResult]`: The per-item result list as returned by
                the portal.
        """
        endpoint = "/api/public/v1/external-asset"
        request_body = [self._serialise_request(item) for item in items]
        response = self._client.post(endpoint, json=request_body)
        payload = self._read_json(response)
        try:
            return _EXTERNAL_ASSET_LIST_ADAPTER.validate_python(payload)
        except ValidationError as validation_error:
            raise ApiResponseError(endpoint, validation_error) from validation_error

    def create_external_network_engagement(
        self,
        request: ExternalNetworkEngagementRequest,
    ) -> EngagementCreated:
        """Creates and launches an external network engagement.

        Args:
            `request` (`ExternalNetworkEngagementRequest`): The request model
                matching the portal-side `CreateExternalEngagementSchema`.
        Returns:
            `EngagementCreated`: The created engagement summary.
        """
        endpoint = "/api/public/v1/engagement/network/external"
        request_body = self._serialise_request(request)
        response = self._client.post(endpoint, json=request_body)
        payload = self._read_json(response)
        return self._validate_response(endpoint, payload, EngagementCreated)

    def create_internal_network_engagement(
        self,
        request: InternalNetworkEngagementRequest,
    ) -> EngagementCreated:
        """Creates and launches an internal network engagement.

        Args:
            `request` (`InternalNetworkEngagementRequest`): The request model
                matching the portal-side `CreateInternalEngagementSchema`.
        Returns:
            `EngagementCreated`: The created engagement summary.
        """
        endpoint = "/api/public/v1/engagement/network/internal"
        request_body = self._serialise_request(request)
        response = self._client.post(endpoint, json=request_body)
        payload = self._read_json(response)
        return self._validate_response(endpoint, payload, EngagementCreated)

    def create_external_web_engagement(
        self,
        request: ExternalWebEngagementRequest,
    ) -> EngagementCreated:
        """Creates and launches an external web engagement.

        Args:
            `request` (`ExternalWebEngagementRequest`): The request model
                matching the portal-side `CreateExternalWebEngagementSchema`.
        Returns:
            `EngagementCreated`: The created engagement summary.
        """
        endpoint = "/api/public/v1/engagement/web/external"
        request_body = self._serialise_request(request)
        response = self._client.post(endpoint, json=request_body)
        payload = self._read_json(response)
        return self._validate_response(endpoint, payload, EngagementCreated)

    def create_internal_web_engagement(
        self,
        request: InternalWebEngagementRequest,
    ) -> EngagementCreated:
        """Creates and launches an internal web engagement.

        Args:
            `request` (`InternalWebEngagementRequest`): The request model
                matching the portal-side `CreateInternalWebEngagementSchema`.
        Returns:
            `EngagementCreated`: The created engagement summary.
        """
        endpoint = "/api/public/v1/engagement/web/internal"
        request_body = self._serialise_request(request)
        response = self._client.post(endpoint, json=request_body)
        payload = self._read_json(response)
        return self._validate_response(endpoint, payload, EngagementCreated)

    @staticmethod
    def _serialise_request(model: BaseModel) -> dict[str, object]:
        """Serialises a Pydantic request model to a JSON-ready dict.

        Omits fields whose value is `None` so optional portal fields accept
        absent keys rather than explicit `null` (Zod `.optional()` semantics).

        Args:
            `model` (`BaseModel`): The request model to serialise.
        Returns:
            `dict[str, object]`: The serialised request body.
        """
        return model.model_dump(mode="json", by_alias=True, exclude_none=True)

    @staticmethod
    def _read_json(response: httpx.Response) -> object:
        """Reads and validates the JSON body of an HTTP response.

        Raises `ApiError` when the response status indicates failure.

        Args:
            `response` (`httpx.Response`): The HTTP response to read.
        Returns:
            `object`: The parsed JSON body on success.
        Raises:
            `ApiError`: When the response status is not successful.
        """
        try:
            body = response.json()
        except ValueError:
            body = None
        if response.is_error:
            error_body: ApiErrorBody | None = None
            if isinstance(body, dict):
                try:
                    error_body = ApiErrorBody.model_validate(body)
                except ValidationError:
                    error_body = None
            message = (
                (error_body.message if error_body else None)
                or response.reason_phrase
                or "Request failed."
            )
            details = error_body.errors if error_body else None
            raise ApiError(
                status_code=response.status_code,
                message=message,
                details=details,
            )
        return body

    @staticmethod
    def _validate_response(
        endpoint: str,
        payload: object,
        model: type[ResponseModelT],
    ) -> ResponseModelT:
        """Validates a successful response payload against a Pydantic model.

        Args:
            `endpoint` (`str`): The API path that returned the payload.
            `payload` (`object`): The parsed JSON body to validate.
            `model` (`type[ResponseModelT]`): The expected response model type.
        Returns:
            `ResponseModelT`: The validated response model instance.
        Raises:
            `ApiResponseError`: When the payload does not match the model.
        """
        try:
            return model.model_validate(payload)
        except ValidationError as validation_error:
            raise ApiResponseError(endpoint, validation_error) from validation_error

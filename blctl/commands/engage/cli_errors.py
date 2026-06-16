"""Defines CLI error handling helpers for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import sys
from collections.abc import Callable
from typing import NoReturn, TypeVar

import click
import httpx

from blctl.api.client import ApiError, ApiResponseError

CallableResultT = TypeVar("CallableResultT")
"""Type variable for the return type of callables passed to `call_or_exit`."""


def exit_with_api_error(error: ApiError) -> NoReturn:
    """Prints an API error to stderr and exits with a non-zero status.

    Args:
        `error` (`ApiError`): The API error to surface.
    """
    click.echo(f"API error: {error}", err=True)
    sys.exit(1)


def exit_with_transport_error(error: httpx.RequestError) -> NoReturn:
    """Prints an HTTP transport error to stderr and exits with a non-zero status.

    Args:
        `error` (`httpx.RequestError`): The underlying httpx transport error.
    """
    click.echo(
        f"Could not reach BreachLock AEV at {error.request.url}: {error}",
        err=True,
    )
    sys.exit(1)


def exit_with_response_error(error: ApiResponseError) -> NoReturn:
    """Prints a response-validation error to stderr and exits with a non-zero status.

    Args:
        `error` (`ApiResponseError`): The validation failure to surface.
    """
    click.echo(str(error), err=True)
    sys.exit(1)


def call_or_exit(thunk: Callable[[], CallableResultT]) -> CallableResultT:
    """Calls `thunk`, converting expected failures into clean stderr messages.

    Args:
        `thunk` (`Callable[[], CallableResultT]`): The no-arg callable to invoke.
    Returns:
        `CallableResultT`: Whatever `thunk` returns on success.
    """
    try:
        return thunk()
    except ApiError as error:
        exit_with_api_error(error)
    except ApiResponseError as error:
        exit_with_response_error(error)
    except httpx.RequestError as error:
        exit_with_transport_error(error)

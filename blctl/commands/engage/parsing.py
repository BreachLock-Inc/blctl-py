"""Defines parsing helpers for the `blctl engage` command.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

import click

from blctl.api.models import NotifyUrl, WebhookHeader


def split_comma_separated(value: str | None) -> list[str]:
    """Splits a comma-separated string into trimmed, non-empty entries.

    Args:
        `value` (`str | None`): The raw value from the command line, or `None`.
    Returns:
        `list[str]`: Trimmed entries, or an empty list when `value` is absent.
    """
    if not value:
        return []
    return [entry.strip() for entry in value.split(",") if entry.strip()]


def parse_notify_url(specification: str) -> NotifyUrl:
    """Parses a `--notify-url` specification into a `NotifyUrl` model.

    The specification is either a bare URL or a URL followed by pipe-separated
    `Name=Value` header pairs.

    Args:
        `specification` (`str`): The raw `--notify-url` value.
    Returns:
        `NotifyUrl`: A model ready to attach to an engagement request.
    Raises:
        `click.BadParameter`: When the specification is empty or malformed.
    """
    segments = [
        segment.strip() for segment in specification.split("|") if segment.strip()
    ]
    if not segments:
        raise click.BadParameter("Notify URL specification is empty.")
    url, *header_segments = segments
    headers: list[WebhookHeader] = []
    for header_segment in header_segments:
        name, separator, header_value = header_segment.partition("=")
        if not separator:
            raise click.BadParameter(
                f"Notify URL header `{header_segment}` must be `Name=Value`."
            )
        headers.append(WebhookHeader(name=name.strip(), value=header_value.strip()))
    return NotifyUrl(url=url, headers=headers)

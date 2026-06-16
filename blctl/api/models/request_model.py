"""Defines the `_RequestModel` base class for outbound public API payloads.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RequestModel(BaseModel):
    """Base class for outbound request models sent to the BreachLock public API."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

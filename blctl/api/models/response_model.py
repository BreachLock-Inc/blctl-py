"""Defines the `_ResponseModel` base class for inbound public API payloads.

Author: Saul Johnson <saul.j@breachlock.com>
Since: 15/06/2026
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ResponseModel(BaseModel):
    """Base class for inbound response models received from the BreachLock public API."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )

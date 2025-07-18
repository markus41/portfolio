from __future__ import annotations

"""Pydantic models used as event payload schemas.

The project originally stored event data in simple ``dataclasses``.  In order
to benefit from input validation and rich error messages we now define these
payloads as :class:`pydantic.BaseModel` subclasses.  The models remain lightweight
and are only concerned with structure validation; they do not implement any
behaviour.
"""

from typing import Any, Dict, List

from pydantic import BaseModel


class LeadCaptureEvent(BaseModel):
    """Event payload for :class:`LeadCaptureAgent`."""

    form_data: Dict[str, Any]
    source: str


class ChatbotEvent(BaseModel):
    """Event payload for :class:`ChatbotAgent`."""

    messages: List[Dict[str, Any]]


class CRMPipelineEvent(BaseModel):
    """Event payload for :class:`CRMPipelineAgent`."""

    deal_id: str
    calendar_id: str
    followup_template: Dict[str, Any]


class SegmentationEvent(BaseModel):
    """Event payload for :class:`SegmentationAdTargetingAgent`."""

    segments: List[Dict[str, Any]]
    budget_per_segment: int


class IntegrationRequest(BaseModel):
    """Event payload for :class:`IntegrationAgent`."""

    name: str


__all__ = [
    "LeadCaptureEvent",
    "ChatbotEvent",
    "CRMPipelineEvent",
    "SegmentationEvent",
    "IntegrationRequest",
]

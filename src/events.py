from __future__ import annotations

"""Event dataclasses used across orchestrators and agents."""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class LeadCaptureEvent:
    """Event payload for :class:`LeadCaptureAgent`."""

    form_data: Dict[str, Any]
    source: str


@dataclass
class ChatbotEvent:
    """Event payload for :class:`ChatbotAgent`."""

    messages: List[Dict[str, Any]]


@dataclass
class CRMPipelineEvent:
    """Event payload for :class:`CRMPipelineAgent`."""

    deal_id: str
    calendar_id: str
    followup_template: Dict[str, Any]


@dataclass
class SegmentationEvent:
    """Event payload for :class:`SegmentationAdTargetingAgent`."""

    segments: List[Dict[str, Any]]
    budget_per_segment: int


@dataclass
class HumanApprovalRequest:
    """Payload for :class:`HumanApprovalAgent`."""

    approval_request: str
    approvers: list[str]
    timeout: int


@dataclass
class NotificationPayload:
    """Payload for :class:`NotificationAgent`."""

    channel: str
    message: str
    platform: str = "slack"


__all__ = [
    "LeadCaptureEvent",
    "ChatbotEvent",
    "CRMPipelineEvent",
    "SegmentationEvent",
    "HumanApprovalRequest",
    "NotificationPayload",
]

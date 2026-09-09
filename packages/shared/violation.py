"""Shared violation type definitions.

Canonical source of truth for Violation/ExamSession types.
API schemas and frontend clients should derive from these definitions.
"""

from enum import Enum


class ViolationType(str, Enum):
    """Violation types detected by the CV pipeline."""

    PHONE = "phone"
    PERSON = "person"
    FACE_LOSS = "face_loss"
    HEAD_TURN = "head_turn"
    VOICE = "voice"
    NOISE = "noise"
    SCREEN_LEAVE = "screen_leave"


class SessionStatus(str, Enum):
    """Exam session lifecycle states."""

    PENDING = "pending"
    ACTIVE = "active"
    ENDED = "ended"


VIOLATION_TYPE_LABELS: dict[ViolationType, str] = {
    ViolationType.PHONE: "Phone detected",
    ViolationType.PERSON: "Unauthorized person",
    ViolationType.FACE_LOSS: "Face not visible",
    ViolationType.HEAD_TURN: "Head turned away",
    ViolationType.VOICE: "Voice detected",
    ViolationType.NOISE: "Background noise",
    ViolationType.SCREEN_LEAVE: "Screen focus lost",
}

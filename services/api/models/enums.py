from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    PROCTOR = "proctor"
    ADMIN = "admin"


class SessionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ENDED = "ended"


class ViolationType(str, Enum):
    PHONE = "phone"
    PERSON = "person"
    FACE_LOSS = "face_loss"
    HEAD_TURN = "head_turn"
    VOICE = "voice"
    NOISE = "noise"
    SCREEN_LEAVE = "screen_leave"
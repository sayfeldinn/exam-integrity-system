from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import SessionStatus

if TYPE_CHECKING:
    from models.student import Student
    from models.violation import Violation


class ExamSession(Base):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    student_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("students.id"),
        nullable=False,
        index=True,
    )
    exam_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    status: Mapped[SessionStatus] = mapped_column(
        SqlEnum(SessionStatus, name="session_status"),
        nullable=False,
        default=SessionStatus.PENDING,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    student: Mapped[Student] = relationship(
        back_populates="sessions",
    )
    violations: Mapped[list[Violation]] = relationship(
        back_populates="session",
    )

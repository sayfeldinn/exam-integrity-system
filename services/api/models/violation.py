from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4


from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import ViolationType


class Violation(Base):
    __tablename__ = "violations"
    __table_args__ = (
        CheckConstraint(
            "risk_contribution >= 0 AND risk_contribution <= 1",
            name="ck_violations_risk_contribution_range",
        ),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_violations_confidence_range",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )
    session_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )
    type: Mapped[ViolationType] = mapped_column(
        SqlEnum(ViolationType, name="violation_type"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    risk_contribution: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    meta: Mapped[dict[str, object]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    session: Mapped["ExamSession"] = relationship(
        back_populates="violations",
    )
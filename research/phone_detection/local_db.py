"""
local_db.py
-----------
Local SQLite database for this feature's development/testing.
Stores confirmed phone-detection violations, separate from any other
feature's database.
"""

import os
from datetime import datetime

from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(__file__), "local_phone_detection.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class PhoneViolation(Base):
    """One confirmed phone-detection violation."""
    __tablename__ = "phone_violations"

    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Creates the table if it does not exist."""
    Base.metadata.create_all(engine)


def log_violation(session_id: str, label: str, confidence: float) -> None:
    import uuid

    session = SessionLocal()
    try:
        session.add(PhoneViolation(
            id=str(uuid.uuid4()),
            session_id=session_id,
            label=label,
            confidence=confidence,
        ))
        session.commit()
    finally:
        session.close()


def get_violations(session_id: str):
    """Returns all logged violations for a session, most recent first."""
    session = SessionLocal()
    try:
        return (
            session.query(PhoneViolation)
            .filter_by(session_id=session_id)
            .order_by(PhoneViolation.created_at.desc())
            .all()
        )
    finally:
        session.close()

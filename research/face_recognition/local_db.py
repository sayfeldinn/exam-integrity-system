"""
local_db.py
-----------
Local SQLite database for storing student data and face embeddings during development.
TEMPORARY dev-only store — will be replaced by Postgres integration.
"""

import json
import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DB_PATH = os.path.join(os.path.dirname(__file__), "local_face_data.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    face_embedding = relationship(
        "StudentFaceEmbedding", back_populates="student", uselist=False
    )


class StudentFaceEmbedding(Base):
    __tablename__ = "student_face_embeddings"

    id = Column(String, primary_key=True)
    student_id = Column(
        String, ForeignKey("students.student_id"), unique=True, nullable=False
    )
    embedding = Column(LargeBinary, nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    student = relationship("Student", back_populates="face_embedding")


def init_db():
    """Creates the tables if they do not exist."""
    Base.metadata.create_all(engine)


def save_face_data(student_id: str, embedding, live_photo_path: str = None):
    """Save or update a student's face embedding."""
    import numpy as np

    session = SessionLocal()
    try:
        embedding_bytes = embedding.astype(np.float32).tobytes()

        student = session.query(Student).filter_by(student_id=student_id).first()
        if not student:
            student = Student(student_id=student_id)
            session.add(student)
            session.commit()

        face_record = (
            session.query(StudentFaceEmbedding)
            .filter_by(student_id=student_id)
            .first()
        )
        if face_record:
            face_record.embedding = embedding_bytes
            face_record.updated_at = datetime.now(timezone.utc)
        else:
            new_face = StudentFaceEmbedding(
                id=str(uuid.uuid4()),
                student_id=student_id,
                embedding=embedding_bytes,
            )
            session.add(new_face)

        session.commit()
    finally:
        session.close()


def get_face_data(student_id: str):
    """Returns (embedding as numpy array, live_photo path) or None if not registered."""
    import numpy as np

    session = SessionLocal()
    try:
        face_record = (
            session.query(StudentFaceEmbedding)
            .filter_by(student_id=student_id)
            .first()
        )
        if face_record is None or not face_record.embedding:
            return None
        embedding = np.frombuffer(face_record.embedding, dtype=np.float32)
        return embedding, None
    finally:
        session.close()

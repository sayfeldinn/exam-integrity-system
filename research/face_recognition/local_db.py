"""
local_db.py
-----------
Local SQLite database for storing student data and face embeddings in separate tables during development.
The embeddings have been separated into a dedicated table linked to the student table.
"""
# NOTE: TEMPORARY dev-only local store -- NOT the shared services/api DB.
# Will be replaced once the real Postgres integration is ready.
import json
import os
import uuid
from datetime import datetime

from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DB_PATH = os.path.join(os.path.dirname(__file__), "local_face_data.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Student(Base):
    """Core students table."""
    __tablename__ = "students"

    student_id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to the face embedding table
    face_embedding = relationship("StudentFaceEmbedding", back_populates="student", uselist=False)


class StudentFaceEmbedding(Base):
    """Separate table for storing face embeddings and live photo references."""
    __tablename__ = "student_face_embeddings"

    id = Column(String, primary_key=True)  # Or could be an auto-increment integer
    student_id = Column(String, ForeignKey("students.student_id"), unique=True, nullable=False)
    live_photo = Column(String(1024))
    embedding = Column(Text)  # Stored as a JSON string
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Reverse relationship back to the student
    student = relationship("Student", back_populates="face_embedding")


def init_db():
    """Creates the tables if they do not exist."""
    Base.metadata.create_all(engine)


def save_face_data(student_id: str, embedding, live_photo_path: str):
    session = SessionLocal()
    try:
        embedding_json = json.dumps(embedding.tolist())
        
        # Ensure the student exists in the student table, otherwise create them
        student = session.query(Student).filter_by(student_id=student_id).first()
        if not student:
            student = Student(student_id=student_id)
            session.add(student)
            session.commit()

        # Update or add embedding data in the separate table
        face_record = session.query(StudentFaceEmbedding).filter_by(student_id=student_id).first()
        if face_record:
            face_record.embedding = embedding_json
            face_record.live_photo = live_photo_path
            face_record.updated_at = datetime.utcnow()
        else:
            new_face = StudentFaceEmbedding(
                id=str(uuid.uuid4()),
                student_id=student_id,
                live_photo=live_photo_path,
                embedding=embedding_json
            )
            session.add(new_face)
            
        session.commit()
    finally:
        session.close()


def get_face_data(student_id: str):
    """Returns (embedding as a numpy array, live_photo path), or None if not registered."""
    import numpy as np

    session = SessionLocal()
    try:
        face_record = session.query(StudentFaceEmbedding).filter_by(student_id=student_id).first()
        if face_record is None or not face_record.embedding:
            return None
        return np.array(json.loads(face_record.embedding)), face_record.live_photo
    finally:
        session.close()
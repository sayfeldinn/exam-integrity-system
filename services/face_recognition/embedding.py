"""
embedding.py
------------
Face detection + alignment + embedding extraction using insightface.
Shared between enrollment.py and recognition.py, hence kept separate.
"""

import numpy as np
from insightface.app import FaceAnalysis

# Loaded once upon module import, not on every extraction call
_face_app = FaceAnalysis(name="buffalo_l")
_face_app.prepare(ctx_id=0, det_size=(640, 640))


def extract_embedding(frame: np.ndarray) -> np.ndarray:
    """
    Takes a frame, detects and aligns the face automatically, and returns the embedding (512-dim vector).
    Raises ValueError if no face is found or if multiple faces are detected.
    """
    faces = _face_app.get(frame)
    if len(faces) == 0:
        raise ValueError("No face detected in this image.")
    if len(faces) > 1:
        raise ValueError("Multiple faces detected in this image.")
    return faces[0].embedding


def average_embeddings(embeddings: list) -> np.ndarray:
    """Takes a list of embeddings from multiple frames and returns their average vector."""
    if not embeddings:
        raise ValueError("No embeddings provided to average.")
    return np.mean(np.array(embeddings), axis=0)
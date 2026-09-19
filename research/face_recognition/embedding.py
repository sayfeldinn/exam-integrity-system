"""
embedding.py
------------
Face detection + alignment + embedding extraction using insightface.
Shared between enrollment and recognition modules.
"""

import numpy as np
from insightface.app import FaceAnalysis


class NoFaceDetected(ValueError):
    """No face found in the frame."""
    pass


class MultipleFacesDetected(ValueError):
    """More than one face found in the frame."""
    pass


_face_app = FaceAnalysis(name="buffalo_l")
_face_app.prepare(ctx_id=0, det_size=(320, 320))


def extract_embedding(frame: np.ndarray) -> np.ndarray:
    faces = _face_app.get(frame)
    if len(faces) == 0:
        raise NoFaceDetected("No face detected in this image.")
    if len(faces) > 1:
        raise MultipleFacesDetected(f"{len(faces)} faces detected in this image.")
    return faces[0].embedding


def average_embeddings(embeddings: list) -> np.ndarray:
    if not embeddings:
        raise ValueError("No embeddings provided to average.")
    return np.mean(np.array(embeddings), axis=0)
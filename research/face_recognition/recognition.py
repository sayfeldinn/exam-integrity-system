"""
recognition.py
--------------
Runtime exam verification logic: current frame -> embedding -> comparison against stored -> decision.
Combines comparison and debouncing logic within the same file.
"""

import time
import numpy as np
from capture import capture_frame, open_camera
from embedding import extract_embedding
from local_db import get_face_data

SIMILARITY_THRESHOLD = 0.8
CONSECUTIVE_MISMATCH_REQUIRED = 2  # Requires consecutive mismatches before flagging a violation


class RecognitionSession:
    """Maintains student session state during the exam to apply debouncing."""

    def __init__(self, student_id: str):
        self.student_id = student_id
        self._consecutive_mismatches = 0

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def check_frame(self, frame) -> dict:
        stored = get_face_data(self.student_id)
        if stored is None:
            raise RuntimeError(f"Student {student_id} is not registered in the database.")
            
        stored_embedding, _ = stored
        
        try:
            current_embedding = extract_embedding(frame)
        except ValueError as e:
            self._consecutive_mismatches += 1
            return {"status": "no_face", "reason": str(e)}
            
        score = self._cosine_similarity(stored_embedding, current_embedding)
        
        if score >= SIMILARITY_THRESHOLD:
            self._consecutive_mismatches = 0
            return {"status": "match", "score": score}
            
        self._consecutive_mismatches += 1
        if self._consecutive_mismatches >= CONSECUTIVE_MISMATCH_REQUIRED:
            self._register_violation(score)
            return {"status": "violation", "score": score}
            
        return {"status": "mismatch", "score": score}

    def _register_violation(self, score: float):
        # Currently prints out; later will link to the real violations table
        print(f"[VIOLATION] Student {self.student_id}: Face mismatch detected (score={score:.2f})")


def run_periodic_check(student_id: str, interval_sec: int = 45, iterations: int = 5):
    """Manual test: periodic check every `interval_sec` seconds, independent of team integration."""
    session = RecognitionSession(student_id)
    cap = open_camera()
    try:
        for i in range(iterations):
            frame = capture_frame(cap)
            result = session.check_frame(frame)
            print(f"[check {i+1}] {result}")
            time.sleep(interval_sec)
    finally:
        cap.release()


if __name__ == "__main__":
    import sys
    sid = sys.argv[1] if len(sys.argv) > 1 else "test-001"
    run_periodic_check(sid, interval_sec=3, iterations=3)
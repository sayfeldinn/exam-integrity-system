"""
enroll_live.py
---------------
Interactive version of enrollment.py — after successful enrollment,
automatically continues into live recognition mode using the same
camera session.
"""

import sys
import cv2
import numpy as np

from embedding import extract_embedding, average_embeddings
from local_db import init_db, save_face_data, get_face_data


THRESHOLD = 0.6


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def run_recognition(cap, student_id: str):
    stored = get_face_data(student_id)
    if stored is None:
        print("No enrollment data found.")
        return
    stored_embedding = stored[0]

    print("Recognition running. Press 'q' in the window to stop.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        try:
            live_embedding = extract_embedding(frame)
            score = cosine_similarity(live_embedding, stored_embedding)
            if score >= THRESHOLD:
                text = f"MATCH - This is you (score={score:.2f})"
                color = (0, 255, 0)
            else:
                text = f"DIFFERENT FACE DETECTED! (score={score:.2f})"
                color = (0, 0, 255)
        except ValueError:
            text = "No face detected"
            color = (0, 165, 255)

        cv2.putText(display, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow("Recognition", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def enroll_student_live(student_id: str, frame_count: int = 1):
    init_db()

    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Could not open the camera.")
        return

    print(f"📸 Camera is active! Click on the camera window first, then press 'c' to capture a frame ({frame_count} required), or 'q' to quit.")

    frames = []
    embeddings = []

    while len(frames) < frame_count:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error reading frame.")
            break

        display = frame.copy()
        cv2.putText(display, f"Captured: {len(frames)}/{frame_count} - press 'c'",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Enrollment - Live", display)

        key = cv2.waitKey(20) & 0xFF

        if key == ord('c'):
            try:
                emb = extract_embedding(frame)
                embeddings.append(emb)
                frames.append(frame)
                print(f"[enroll] Frame {len(frames)}: Embedding extracted successfully ✅")
            except ValueError as e:
                print(f"[enroll] Frame ignored: {e}")
        elif key == ord('q'):
            print("Cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return

    cv2.destroyWindow("Enrollment - Live")

    if not embeddings:
        cap.release()
        cv2.destroyAllWindows()
        raise RuntimeError("Could not extract any valid embedding from the frames. Please try again.")

    final_embedding = average_embeddings(embeddings)
    
    save_face_data(student_id, final_embedding, None)

    print(f"[enroll] Student {student_id} enrolled successfully ✅")
    print("Moving to recognition mode...")

    # camera stays open — straight into recognition, no need to reopen
    run_recognition(cap, student_id)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "test-001"
    enroll_student_live(sid)
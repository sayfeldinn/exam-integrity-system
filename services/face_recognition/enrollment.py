"""
enroll_live.py
---------------
Interactive version of enrollment.py
"""

import sys
import cv2

from embedding import extract_embedding, average_embeddings
from local_db import init_db, save_face_data
from capture import save_live_photo


def enroll_student_live(student_id: str, frame_count: int = 5):
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
        cv2.setWindowProperty("Enrollment - Live", cv2.WND_PROP_TOPMOST, 1)

        key = cv2.waitKey(20) & 0xFF

        if key != 255:  # If any key was actually pressed
            print(f"[debug] key pressed code: {key}")

        if key == ord('c'):
            print("[debug] 'c' pressed, trying to extract embedding...")
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

    cap.release()
    cv2.destroyAllWindows()

    if not embeddings:
        raise RuntimeError("Could not extract any valid embedding from the frames. Please try again.")

    final_embedding = average_embeddings(embeddings)
    live_photo_path = save_live_photo(frames[0], student_id)
    save_face_data(student_id, final_embedding, live_photo_path)

    print(f"[enroll] Student {student_id} enrolled successfully ✅")
    return final_embedding


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "test-001"
    enroll_student_live(sid)
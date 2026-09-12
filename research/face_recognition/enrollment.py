"""
enrollment.py
-------------
Interactive enrollment: capture frames, extract embeddings, store in local DB.
Optionally continues into live recognition mode after enrollment.
"""

import sys

import cv2

from capture import open_camera
from embedding import extract_embedding, average_embeddings
from local_db import init_db, save_face_data, get_face_data
from recognition import cosine_similarity, SIMILARITY_THRESHOLD


def enroll_student(
    student_id: str,
    frame_count: int = 5,
    run_recognition: bool = False,
):
    """Enroll a student by capturing frames and extracting face embeddings.

    Args:
        student_id: Unique identifier for the student.
        frame_count: Number of frames to capture for averaging.
        run_recognition: If True, continue into recognition mode after enrollment.
    """
    init_db()

    cap = open_camera()
    print(
        f"Camera active! Press 'c' to capture a frame ({frame_count} needed), "
        f"or 'q' to quit."
    )

    frames = []
    embeddings = []

    try:
        while len(frames) < frame_count:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame.")
                break

            display = frame.copy()
            cv2.putText(
                display,
                f"Captured: {len(frames)}/{frame_count} - press 'c'",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Enrollment", display)

            key = cv2.waitKey(20) & 0xFF

            if key == ord("c"):
                try:
                    emb = extract_embedding(frame)
                    embeddings.append(emb)
                    frames.append(frame)
                    print(
                        f"[enroll] Frame {len(frames)}: Embedding extracted OK"
                    )
                except ValueError as e:
                    print(f"[enroll] Frame ignored: {e}")
            elif key == ord("q"):
                print("Cancelled.")
                return None

        cv2.destroyWindow("Enrollment")

        if not embeddings:
            raise RuntimeError(
                "Could not extract any valid embedding from the frames."
            )

        final_embedding = average_embeddings(embeddings)
        save_face_data(student_id, final_embedding, None)
        print(f"[enroll] Student {student_id} enrolled successfully")

        if run_recognition:
            print("Moving to recognition mode...")
            _run_recognition_loop(cap, student_id)

        return final_embedding

    finally:
        cap.release()
        cv2.destroyAllWindows()


def _run_recognition_loop(cap, student_id: str):
    """Run live recognition using the already-open camera."""
    stored = get_face_data(student_id)
    if stored is None:
        print("No enrollment data found.")
        return

    stored_embedding = stored[0]
    print("Recognition running. Press 'q' to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        try:
            from embedding import extract_embedding as _extract

            live_embedding = _extract(frame)
            score = cosine_similarity(live_embedding, stored_embedding)
            if score >= SIMILARITY_THRESHOLD:
                text = f"MATCH (score={score:.2f})"
                color = (0, 255, 0)
            else:
                text = f"MISMATCH (score={score:.2f})"
                color = (0, 0, 255)
        except ValueError:
            text = "No face detected"
            color = (0, 165, 255)

        cv2.putText(
            display, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
        )
        cv2.imshow("Recognition", display)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "test-001"
    enroll_student(sid, frame_count=5, run_recognition=False)

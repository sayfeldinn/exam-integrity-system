# Face Visibility Monitor

> **Superseded** by `research/face_recognition/` which includes face detection, embedding, enrollment, and recognition. This module is retained for reference only.

This module monitors face visibility in real-time using OpenCV and MediaPipe for the exam integrity system.

## How to Run

1. **Install Dependencies:**
   Make sure you are in the project environment, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Monitor:**
   ```bash
   python monitor.py
   ```

The monitor will open a camera window and display real-time face visibility status.

## Status

Superseded by `face_recognition` which provides full enrollment + recognition pipeline with InsightFace.

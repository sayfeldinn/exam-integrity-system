

"""
Face Detection and Face Visibility Monitoring Module
======================================================
 
Part of a Computer-Vision-based exam proctoring / cheating detection
pipeline. This module is self-contained and exposes a clean API
(`FaceVisibilityMonitor`) so it can be dropped into a larger system
(Face Recognition, Head Pose Estimation, Gaze Tracking, Object
Detection, Cheating Event Detection, ...) without depending on a
live webcam or a display window.
 
Author: Generated for academic / graduation-project use.
"""
 
from __future__ import annotations
 
import time
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional, Tuple
 
import cv2
import numpy as np
import mediapipe as mp
 
 
# =====================================================================
# 1. Enums & Data Structures
# =====================================================================
 
class SystemStatus(Enum):
    """Overall status of the proctoring face-visibility subsystem."""
    NORMAL = "NORMAL"
    NO_FACE = "NO FACE"
    MULTIPLE_FACES = "MULTIPLE FACES"
    FACE_OUT_OF_FRAME = "FACE OUT OF FRAME"
    FACE_OCCLUDED = "FACE OCCLUDED"
    POOR_VISIBILITY = "POOR VISIBILITY"
 
 
WARNING_MESSAGES = {
    SystemStatus.NO_FACE: "WARNING: No face detected.",
    SystemStatus.MULTIPLE_FACES: "WARNING: Multiple faces detected.",
    SystemStatus.FACE_OUT_OF_FRAME: "WARNING: Please keep your entire face inside the frame.",
    SystemStatus.FACE_OCCLUDED: "WARNING: Face is partially covered.",
    SystemStatus.POOR_VISIBILITY: "WARNING: Face visibility is insufficient.",
}
 
# Priority (most severe first). Used only for documentation / logging;
# the actual evaluation order is encoded directly in the analysis logic.
STATUS_SEVERITY_ORDER = [
    SystemStatus.NO_FACE,
    SystemStatus.MULTIPLE_FACES,
    SystemStatus.FACE_OUT_OF_FRAME,
    SystemStatus.FACE_OCCLUDED,
    SystemStatus.POOR_VISIBILITY,
    SystemStatus.NORMAL,
]
 
# Colors (BGR) used for on-screen rendering.
STATUS_COLORS = {
    SystemStatus.NORMAL: (0, 200, 0),
    SystemStatus.NO_FACE: (0, 0, 220),
    SystemStatus.MULTIPLE_FACES: (0, 140, 255),
    SystemStatus.FACE_OUT_OF_FRAME: (0, 140, 255),
    SystemStatus.FACE_OCCLUDED: (0, 0, 220),
    SystemStatus.POOR_VISIBILITY: (0, 165, 255),
}
 
 
@dataclass
class FaceObservation:
    """A single detected face for the current frame."""
    bbox: Tuple[int, int, int, int]        # (x_min, y_min, x_max, y_max) px
    landmarks_px: np.ndarray               # (N, 2) int pixel coordinates
    landmarks_norm: np.ndarray             # (N, 3) normalized (x, y, z)
    detection_score: float = 1.0           # approximate mesh confidence
 
 
@dataclass
class VisibilityMetrics:
    blur_score: float = 0.0
    brightness: float = 0.0
    yaw_deg: float = 0.0
    pitch_deg: float = 0.0
    roll_deg: float = 0.0
    occluded_region_ratio: float = 0.0
    occluded_regions: List[str] = field(default_factory=list)
    # raw {"variance": float, "edge_density": float} per macro region,
    # used to both judge occlusion and update the adaptive baseline.
    region_scores: dict = field(default_factory=dict)
 
 
@dataclass
class FrameAnalysisResult:
    """Everything downstream pipeline stages need for this frame."""
    raw_status: SystemStatus
    confirmed_status: SystemStatus         # after temporal debouncing
    warning_message: Optional[str]
    face_count: int
    faces: List[FaceObservation]
    metrics: Optional[VisibilityMetrics]
    timestamp: float = field(default_factory=time.time)
 
 
# =====================================================================
# 2. Configuration
# =====================================================================
 
@dataclass
class MonitorConfig:
    # --- Capture ---
    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720
 
    # --- Detection ---
    max_faces_to_track: int = 5            # cap on faces the mesh model tracks
    min_detection_confidence: float = 0.5
    min_tracking_confidence: float = 0.5
 
    # --- Frame boundary validation ---
    # frame_margin_ratio is intentionally NOT near-zero: a small buffer
    # means the alert fires as soon as ANY part of the face reaches the
    # edge zone, rather than waiting until it is almost entirely gone.
    frame_margin_ratio: float = 0.025      # min gap to frame edge (fraction of dim)
    face_area_min_ratio: float = 0.035     # below -> face too far away (separate check, off by default)
    face_area_max_ratio: float = 0.55      # above -> face too close (separate check, off by default)
 
    # --- Visibility / quality ---
    blur_threshold: float = 60.0           # Laplacian variance below -> blurry
    brightness_min: float = 40.0           # mean intensity below -> too dark
    brightness_max: float = 235.0          # mean intensity above -> overexposed
    max_yaw_deg: float = 35.0
    max_pitch_deg: float = 25.0
    max_roll_deg: float = 30.0
 
    # --- Alerting scope ---
    # Current requirement: warnings for NO_FACE, MULTIPLE_FACES,
    # sustained FACE_OCCLUDED, and a face part leaving the frame edge
    # (FACE_OUT_OF_FRAME, edge-clip check only -- NOT the too-close/far
    # size check, which stays off to avoid firing during normal seating).
    enable_boundary_alerts: bool = True
    enable_quality_alerts: bool = False
 
    # --- Temporal debouncing (wall-clock seconds, NOT frame counts, so
    # behaviour no longer depends on camera FPS) ---
    presence_alert_delay_sec: float = 0.3    # NO_FACE / MULTIPLE_FACES / recovery
    occlusion_alert_delay_sec: float = 2.0   # coverage must persist this long
 
    # --- Occlusion: adaptive, self-calibrating ---
    # Rather than fixed magic-number thresholds (which break across
    # different skin tones / cameras / lighting), each macro region's
    # "normal" texture level is learned live via EMA while the face is
    # confirmed visible. Occlusion is then flagged as a large *relative*
    # drop from that personal baseline.
    occlusion_patch_size: int = 64
    occlusion_baseline_ema_alpha: float = 0.05
    occlusion_relative_drop_threshold: float = 0.45   # texture: flag if < 45% of baseline
    occlusion_min_baseline_samples: int = 20          # ~0.7-1s of "normal" frames
    # Detector-confidence signal (independent of texture): flag if the
    # BlazeFace detection score falls under this fraction of its learned
    # baseline. Kept gentler than the texture ratio since confidence
    # naturally varies a bit more from frame to frame.
    occlusion_confidence_drop_threshold: float = 0.75
 
    def frame_area(self) -> int:
        return self.frame_width * self.frame_height
 
 
# =====================================================================
# 3. Facial landmark region groups (MediaPipe FaceMesh, 468-point model)
# =====================================================================
# These groups define coarse regions used for occlusion analysis.
# Index sets are the widely-used MediaPipe FaceMesh topology groupings.
 
LEFT_EYE_IDX = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE_IDX = [263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384, 385, 386, 387, 388, 466]
MOUTH_IDX = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78]
NOSE_IDX = [1, 2, 98, 327, 168, 6, 197, 195, 5, 4, 45, 275]
CHIN_IDX = [152, 175, 199, 200, 18]
 
# Two large, contiguous macro-regions instead of five small ones. A hand,
# mask, or paper typically covers a broad area at once (eyes+brows, or
# nose+mouth+chin) -- grouping landmarks this way makes the texture-drop
# signal much stronger and less sensitive to small per-point noise than
# many tiny regions ever could be.
OCCLUSION_MACRO_REGIONS = {
    "eyes_region": LEFT_EYE_IDX + RIGHT_EYE_IDX,
    "lower_face_region": NOSE_IDX + MOUTH_IDX + CHIN_IDX,
}
 
# 6-point model for head pose (solvePnP): generic anthropometric 3D points.
HEAD_POSE_LANDMARK_IDX = {
    "nose_tip": 1,
    "chin": 152,
    "left_eye_left_corner": 33,
    "right_eye_right_corner": 263,
    "left_mouth_corner": 61,
    "right_mouth_corner": 291,
}
 
HEAD_POSE_MODEL_POINTS_3D = np.array([
    (0.0, 0.0, 0.0),            # Nose tip
    (0.0, -330.0, -65.0),       # Chin
    (-225.0, 170.0, -135.0),    # Left eye, left corner
    (225.0, 170.0, -135.0),     # Right eye, right corner
    (-150.0, -150.0, -125.0),   # Left mouth corner
    (150.0, -150.0, -125.0),    # Right mouth corner
], dtype=np.float64)
 
 
# =====================================================================
# 4. Face Detection (MediaPipe FaceMesh wrapper)
# =====================================================================
 
class FaceMeshDetector:
    """
    Wraps MediaPipe FaceMesh (dense landmarks) together with MediaPipe's
    lightweight Face Detection model (BlazeFace). FaceMesh supplies
    landmarks for boundary/head-pose/texture analysis; Face Detection
    supplies an independent per-face confidence score that is used as a
    second, structurally different occlusion signal (see
    VisibilityAnalyzer) -- it is trained to recognize a face by its key
    features (eyes, nose, mouth corners), so its confidence measurably
    drops when those features are hidden, even if FaceMesh itself keeps
    reporting plausible landmark positions.
    """
 
    def __init__(self, config: MonitorConfig):
        self._config = config
        self._mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=config.max_faces_to_track,
            refine_landmarks=True,
            min_detection_confidence=config.min_detection_confidence,
            min_tracking_confidence=config.min_tracking_confidence,
        )
        self._face_detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.3,  # deliberately low: we want the
        )                                   # score itself, not a hard cutoff
 
    @staticmethod
    def _bbox_iou(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float]) -> float:
        ax_min, ay_min, ax_max, ay_max = a
        bx_min, by_min, bx_max, by_max = b
        ix_min, iy_min = max(ax_min, bx_min), max(ay_min, by_min)
        ix_max, iy_max = min(ax_max, bx_max), min(ay_max, by_max)
        inter = max(0.0, ix_max - ix_min) * max(0.0, iy_max - iy_min)
        area_a = max(0.0, ax_max - ax_min) * max(0.0, ay_max - ay_min)
        area_b = max(0.0, bx_max - bx_min) * max(0.0, by_max - by_min)
        union = area_a + area_b - inter
        return inter / union if union > 0 else 0.0
 
    def _match_detection_score(
        self, landmarks_px: np.ndarray, detections, frame_size: Tuple[int, int]
    ) -> float:
        if not detections:
            return 1.0
        w, h = frame_size
        mesh_box = (
            float(landmarks_px[:, 0].min()), float(landmarks_px[:, 1].min()),
            float(landmarks_px[:, 0].max()), float(landmarks_px[:, 1].max()),
        )
        best_iou, best_score = 0.0, 1.0
        for det in detections:
            rb = det.location_data.relative_bounding_box
            det_box = (rb.xmin * w, rb.ymin * h, (rb.xmin + rb.width) * w, (rb.ymin + rb.height) * h)
            iou = self._bbox_iou(mesh_box, det_box)
            if iou > best_iou:
                best_iou = iou
                best_score = float(det.score[0]) if det.score else 1.0
        return best_score
 
    def process(self, frame_bgr: np.ndarray) -> List[FaceObservation]:
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
 
        mesh_results = self._mesh.process(rgb)
        detections = self._face_detector.process(rgb).detections or []
 
        observations: List[FaceObservation] = []
        if not mesh_results.multi_face_landmarks:
            return observations
 
        for face_landmarks in mesh_results.multi_face_landmarks:
            norm = np.array(
                [(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark],
                dtype=np.float64,
            )
            px = np.stack([norm[:, 0] * w, norm[:, 1] * h], axis=1).astype(np.int32)
 
            x_min, y_min = px[:, 0].min(), px[:, 1].min()
            x_max, y_max = px[:, 0].max(), px[:, 1].max()
            detection_score = self._match_detection_score(px, detections, (w, h))
 
            observations.append(
                FaceObservation(
                    bbox=(int(x_min), int(y_min), int(x_max), int(y_max)),
                    landmarks_px=px,
                    landmarks_norm=norm,
                    detection_score=detection_score,
                )
            )
        return observations
 
    def close(self):
        self._mesh.close()
        self._face_detector.close()
 
 
# =====================================================================
# 5. Frame Boundary Validation
# =====================================================================
 
class FrameBoundaryValidator:
    """
    Determines whether a detected face is fully contained within the
    camera frame. Two independent checks are exposed:
 
    - `is_edge_clipped`: any part of the face landmarks reaches the
      configured margin near a frame edge -- i.e. a part of the face is
      (or is about to be) literally outside the visible frame. This is
      what drives the FACE_OUT_OF_FRAME alert.
    - `is_out_of_size_range`: the face is disproportionately large/small
      relative to the frame (too close / too far). Kept separate and
      not alert-driving by default, since "too close/far" is a framing
      *quality* concern rather than "part of the face left the camera".
    """
 
    def __init__(self, config: MonitorConfig):
        self._config = config
 
    def is_edge_clipped(self, bbox: Tuple[int, int, int, int], frame_size: Tuple[int, int]) -> bool:
        x_min, y_min, x_max, y_max = bbox
        w, h = frame_size
        margin_x = int(w * self._config.frame_margin_ratio)
        margin_y = int(h * self._config.frame_margin_ratio)
        return (
            x_min <= margin_x
            or y_min <= margin_y
            or x_max >= (w - margin_x)
            or y_max >= (h - margin_y)
        )
 
    def is_out_of_size_range(self, bbox: Tuple[int, int, int, int], frame_size: Tuple[int, int]) -> bool:
        x_min, y_min, x_max, y_max = bbox
        w, h = frame_size
        face_area = max(0, (x_max - x_min)) * max(0, (y_max - y_min))
        area_ratio = face_area / float(w * h)
        return area_ratio < self._config.face_area_min_ratio or area_ratio > self._config.face_area_max_ratio
 
    def is_out_of_frame(self, bbox: Tuple[int, int, int, int], frame_size: Tuple[int, int]) -> bool:
        """Backward-compatible combined check (edge-clipped OR bad size)."""
        return self.is_edge_clipped(bbox, frame_size) or self.is_out_of_size_range(bbox, frame_size)
 
 
# =====================================================================
# 6. Visibility / Occlusion / Head-Pose Analysis
# =====================================================================
 
class VisibilityAnalyzer:
    """
    Given a frame and a single FaceObservation, computes quantitative
    visibility metrics: sharpness, brightness, head pose, and a
    region-based occlusion score.
 
    Occlusion heuristic
    --------------------
    Facial regions that are naturally rich in local texture/edges
    (eyes, mouth, nose bridge, chin) lose that texture when covered by
    a hand, mask or other object -- the covering surface is comparatively
    flat and low-contrast. For each region we crop the landmark-bounded
    patch and measure (a) edge density (Canny) and (b) local intensity
    variance (Laplacian). A region is flagged "occluded" when both
    signals fall below their configured thresholds. The face is
    considered occluded once enough regions are flagged.
    """
 
    def __init__(self, config: MonitorConfig):
        self._config = config
        # Per-region learned "normal" texture level and detector-confidence
        # level: {region: {"variance":, "edge_density":}}, {"conf": float}
        self._baseline: dict = {}
        self._baseline_samples: dict = {}
        self._conf_baseline: Optional[float] = None
        self._conf_baseline_samples: int = 0
 
    # ---- Sharpness ---------------------------------------------------
    @staticmethod
    def _laplacian_variance(gray_patch: np.ndarray) -> float:
        if gray_patch.size == 0:
            return 0.0
        return float(cv2.Laplacian(gray_patch, cv2.CV_64F).var())
 
    # ---- Brightness ----------------------------------------------------
    @staticmethod
    def _mean_brightness(gray_patch: np.ndarray) -> float:
        if gray_patch.size == 0:
            return 0.0
        return float(gray_patch.mean())
 
    # ---- Head pose -----------------------------------------------------
    def _estimate_head_pose(
        self, face: FaceObservation, frame_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        w, h = frame_size
        idx = HEAD_POSE_LANDMARK_IDX
        image_points = np.array([
            face.landmarks_px[idx["nose_tip"]],
            face.landmarks_px[idx["chin"]],
            face.landmarks_px[idx["left_eye_left_corner"]],
            face.landmarks_px[idx["right_eye_right_corner"]],
            face.landmarks_px[idx["left_mouth_corner"]],
            face.landmarks_px[idx["right_mouth_corner"]],
        ], dtype=np.float64)
 
        focal_length = w
        center = (w / 2.0, h / 2.0)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1],
        ], dtype=np.float64)
        dist_coeffs = np.zeros((4, 1))
 
        success, rotation_vec, _ = cv2.solvePnP(
            HEAD_POSE_MODEL_POINTS_3D,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if not success:
            return 0.0, 0.0, 0.0
 
        rotation_mat, _ = cv2.Rodrigues(rotation_vec)
        pose_mat = cv2.hconcat((rotation_mat, np.zeros((3, 1))))
        _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(pose_mat)
        pitch, yaw, roll = [float(a) for a in euler_angles.flatten()]
        return yaw, pitch, roll
 
    # ---- Occlusion: texture signal --------------------------------------
 
    def _region_bbox(self, face: FaceObservation, idxs: List[int], pad_ratio: float = 0.15) -> Tuple[int, int, int, int]:
        pts = face.landmarks_px[idxs]
        x_min, y_min = pts[:, 0].min(), pts[:, 1].min()
        x_max, y_max = pts[:, 0].max(), pts[:, 1].max()
        pad_x = max(2, int((x_max - x_min) * pad_ratio))
        pad_y = max(2, int((y_max - y_min) * pad_ratio))
        return x_min - pad_x, y_min - pad_y, x_max + pad_x, y_max + pad_y
 
    def _region_metrics(self, gray_frame: np.ndarray, face: FaceObservation, idxs: List[int]) -> Optional[dict]:
        h, w = gray_frame.shape[:2]
        patch_size = self._config.occlusion_patch_size
        x_min, y_min, x_max, y_max = self._region_bbox(face, idxs)
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_max, y_max = min(w, x_max), min(h, y_max)
        patch = gray_frame[y_min:y_max, x_min:x_max]
        if patch.size == 0:
            return None
 
        # Normalize size so metrics are comparable regardless of distance
        # from camera / capture resolution. NOTE: histogram equalization
        # was deliberately removed here -- it stretches contrast even on
        # a genuinely flat/covered patch, turning ordinary sensor noise
        # into fake "edges" and defeating the whole signal. A mild median
        # blur instead suppresses noise without inventing texture.
        patch = cv2.resize(patch, (patch_size, patch_size), interpolation=cv2.INTER_AREA)
        patch = cv2.medianBlur(patch, 3)
 
        variance = self._laplacian_variance(patch)
        edges = cv2.Canny(patch, 40, 120)
        edge_density = float(np.count_nonzero(edges)) / float(patch.size)
        return {"variance": variance, "edge_density": edge_density}
 
    def compute_region_scores(self, gray_frame: np.ndarray, face: FaceObservation) -> dict:
        scores = {}
        for name, idxs in OCCLUSION_MACRO_REGIONS.items():
            m = self._region_metrics(gray_frame, face, idxs)
            if m is not None:
                scores[name] = m
        return scores
 
    def update_baseline(self, region_scores: dict) -> None:
        """Slowly learn each region's 'normal' texture level (EMA). Call
        this only for frames already confirmed to show a normal, visible
        face -- never while occlusion is suspected, or the baseline would
        drift toward the occluded state during a sustained cover-up."""
        alpha = self._config.occlusion_baseline_ema_alpha
        for name, vals in region_scores.items():
            if name not in self._baseline:
                self._baseline[name] = dict(vals)
                self._baseline_samples[name] = 1
            else:
                b = self._baseline[name]
                b["variance"] = (1 - alpha) * b["variance"] + alpha * vals["variance"]
                b["edge_density"] = (1 - alpha) * b["edge_density"] + alpha * vals["edge_density"]
                self._baseline_samples[name] = self._baseline_samples.get(name, 0) + 1
 
    def evaluate_occlusion(self, region_scores: dict) -> List[str]:
        """Flag a region as occluded when BOTH its texture variance and
        edge density have dropped well below (a configurable fraction of)
        this session's own learned baseline for that region. Regions
        without enough baseline samples yet are skipped (not yet judged),
        which naturally gives the system a short calibration warm-up."""
        cfg = self._config
        flagged: List[str] = []
        for name, vals in region_scores.items():
            baseline = self._baseline.get(name)
            samples = self._baseline_samples.get(name, 0)
            if baseline is None or samples < cfg.occlusion_min_baseline_samples:
                continue
            var_dropped = vals["variance"] < baseline["variance"] * cfg.occlusion_relative_drop_threshold
            edge_dropped = vals["edge_density"] < baseline["edge_density"] * cfg.occlusion_relative_drop_threshold
            if var_dropped and edge_dropped:
                flagged.append(name)
        return flagged
 
    # ---- Occlusion: independent detector-confidence signal --------------
    def update_confidence_baseline(self, detection_score: float) -> None:
        """Learn this session's normal BlazeFace detection-confidence
        level, same EMA/freeze-while-suspect discipline as the texture
        baseline above."""
        alpha = self._config.occlusion_baseline_ema_alpha
        if self._conf_baseline is None:
            self._conf_baseline = detection_score
        else:
            self._conf_baseline = (1 - alpha) * self._conf_baseline + alpha * detection_score
        self._conf_baseline_samples += 1
 
    def is_confidence_dropped(self, detection_score: float) -> bool:
        """A structurally different signal from the texture check: the
        BlazeFace detector itself relies on recognizing eyes/nose/mouth
        keypoints, so its confidence drops when they're hidden -- even
        for cases (e.g. certain masks) where local texture alone is
        ambiguous."""
        cfg = self._config
        if self._conf_baseline is None or self._conf_baseline_samples < cfg.occlusion_min_baseline_samples:
            return False
        return detection_score < self._conf_baseline * cfg.occlusion_confidence_drop_threshold
 
    # ---- Public entry point --------------------------------------------
    def analyze(self, frame_bgr: np.ndarray, face: FaceObservation) -> VisibilityMetrics:
        h, w = frame_bgr.shape[:2]
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
 
        x_min, y_min, x_max, y_max = face.bbox
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_max, y_max = min(w, x_max), min(h, y_max)
        face_patch = gray[y_min:y_max, x_min:x_max]
 
        blur_score = self._laplacian_variance(face_patch)
        brightness = self._mean_brightness(face_patch)
        yaw, pitch, roll = self._estimate_head_pose(face, (w, h))
        region_scores = self.compute_region_scores(gray, face)
 
        return VisibilityMetrics(
            blur_score=blur_score,
            brightness=brightness,
            yaw_deg=yaw,
            pitch_deg=pitch,
            roll_deg=roll,
            region_scores=region_scores,
        )
 
    def is_poor_visibility(self, metrics: VisibilityMetrics) -> bool:
        cfg = self._config
        return (
            metrics.blur_score < cfg.blur_threshold
            or not (cfg.brightness_min <= metrics.brightness <= cfg.brightness_max)
            or abs(_angle_wrap(metrics.yaw_deg)) > cfg.max_yaw_deg
            or abs(_angle_wrap(metrics.pitch_deg)) > cfg.max_pitch_deg
            or abs(_angle_wrap(metrics.roll_deg)) > cfg.max_roll_deg
        )
 
 
def _angle_wrap(angle_deg: float) -> float:
    """Wrap an angle to the [-90, 90] range (decomposeProjectionMatrix quirk)."""
    a = angle_deg
    if a < -90:
        a += 180
    elif a > 90:
        a -= 180
    return a
 
 
# =====================================================================
# 7. Temporal Debouncing
# =====================================================================
 
class StatusDebouncer:
    """
    Requires a raw status to persist for a configured *wall-clock*
    duration (in either direction: onset or recovery) before it becomes
    the "confirmed" status that triggers a warning. Using real seconds
    rather than a frame count means behaviour stays correct regardless
    of camera FPS. Different statuses can require different delays --
    e.g. NO_FACE/MULTIPLE_FACES confirm almost immediately, while
    FACE_OCCLUDED requires a couple of full seconds of sustained
    coverage before it counts as a real cheating-relevant event.
    """
 
    def __init__(self, required_delay_by_status: dict, default_delay_sec: float = 0.3):
        self._required_delay = required_delay_by_status
        self._default_delay = default_delay_sec
        self._candidate: Optional[SystemStatus] = None
        self._candidate_since: Optional[float] = None
        self._confirmed = SystemStatus.NORMAL
 
    def update(self, raw_status: SystemStatus, now: Optional[float] = None) -> SystemStatus:
        now = now if now is not None else time.time()
 
        if raw_status != self._candidate:
            self._candidate = raw_status
            self._candidate_since = now
 
        elapsed = now - self._candidate_since
        required = self._required_delay.get(raw_status, self._default_delay)
        if elapsed >= required:
            self._confirmed = raw_status
 
        return self._confirmed
 
    def reset(self):
        self._candidate = None
        self._candidate_since = None
        self._confirmed = SystemStatus.NORMAL
 
 
# =====================================================================
# 8. Main Orchestrator
# =====================================================================
 
class FaceVisibilityMonitor:
    """
    High-level, pipeline-friendly entry point. Owns no camera and no
    display window -- callers feed it frames via `analyze()` and get a
    structured `FrameAnalysisResult` back. This makes it trivial to
    plug into a larger proctoring system that already owns the capture
    loop and orchestrates multiple modules (face recognition, gaze
    tracking, object detection, etc.).
    """
 
    def __init__(
        self,
        config: Optional[MonitorConfig] = None,
        on_status_change: Optional[Callable[[SystemStatus, Optional[str]], None]] = None,
    ):
        self.config = config or MonitorConfig()
        self._detector = FaceMeshDetector(self.config)
        self._boundary_validator = FrameBoundaryValidator(self.config)
        self._visibility_analyzer = VisibilityAnalyzer(self.config)
        self._debouncer = StatusDebouncer(
            required_delay_by_status={
                SystemStatus.NO_FACE: self.config.presence_alert_delay_sec,
                SystemStatus.MULTIPLE_FACES: self.config.presence_alert_delay_sec,
                SystemStatus.FACE_OCCLUDED: self.config.occlusion_alert_delay_sec,
                SystemStatus.NORMAL: self.config.presence_alert_delay_sec,
            },
            default_delay_sec=self.config.presence_alert_delay_sec,
        )
        self.on_status_change = on_status_change
        self._last_confirmed = SystemStatus.NORMAL
 
    def analyze(self, frame_bgr: np.ndarray) -> FrameAnalysisResult:
        h, w = frame_bgr.shape[:2]
        faces = self._detector.process(frame_bgr)
        face_count = len(faces)
        metrics: Optional[VisibilityMetrics] = None
 
        if face_count == 0:
            raw_status = SystemStatus.NO_FACE
        elif face_count > 1:
            raw_status = SystemStatus.MULTIPLE_FACES
        else:
            face = faces[0]
            metrics = self._visibility_analyzer.analyze(frame_bgr, face)
            flagged_regions = self._visibility_analyzer.evaluate_occlusion(metrics.region_scores)
            confidence_dropped = self._visibility_analyzer.is_confidence_dropped(face.detection_score)
            if confidence_dropped:
                flagged_regions = flagged_regions + ["detector_confidence"]
            metrics.occluded_regions = flagged_regions
            metrics.occluded_region_ratio = (
                len(flagged_regions) / (len(metrics.region_scores) + 1) if metrics.region_scores else 0.0
            )
 
            if flagged_regions:
                # Either signal is enough on its own: a large sustained
                # texture drop in one macro region (eyes, or nose+mouth+
                # chin), OR a sustained drop in the independent face-
                # detector confidence -- both indicate a significant part
                # of the face is no longer genuinely visible.
                raw_status = SystemStatus.FACE_OCCLUDED
            elif self.config.enable_boundary_alerts and self._boundary_validator.is_edge_clipped(face.bbox, (w, h)):
                raw_status = SystemStatus.FACE_OUT_OF_FRAME
            elif self.config.enable_quality_alerts and self._visibility_analyzer.is_poor_visibility(metrics):
                raw_status = SystemStatus.POOR_VISIBILITY
            else:
                raw_status = SystemStatus.NORMAL
 
            # Only ever learn "what normal looks like" from a frame that is
            # NOT even momentarily suspected of occlusion -- otherwise a
            # sustained cover-up would slowly drag the baseline down to
            # match the occluded state and the check would stop working.
            if raw_status == SystemStatus.NORMAL:
                self._visibility_analyzer.update_baseline(metrics.region_scores)
                self._visibility_analyzer.update_confidence_baseline(face.detection_score)
 
        confirmed_status = self._debouncer.update(raw_status)
 
        if confirmed_status != self._last_confirmed:
            self._last_confirmed = confirmed_status
            if self.on_status_change:
                self.on_status_change(confirmed_status, WARNING_MESSAGES.get(confirmed_status))
 
        # Alerting scope: only these three statuses are surfaced as
        # warnings; everything else (including in-progress framing/quality
        # issues when those checks are disabled) reports NORMAL / no warning.
        alertable = {SystemStatus.NO_FACE, SystemStatus.MULTIPLE_FACES, SystemStatus.FACE_OCCLUDED}
        if self.config.enable_boundary_alerts:
            alertable.add(SystemStatus.FACE_OUT_OF_FRAME)
        if self.config.enable_quality_alerts:
            alertable.add(SystemStatus.POOR_VISIBILITY)
 
        display_status = confirmed_status if confirmed_status in alertable else SystemStatus.NORMAL
        warning_message = WARNING_MESSAGES.get(confirmed_status) if confirmed_status in alertable else None
 
        return FrameAnalysisResult(
            raw_status=raw_status,
            confirmed_status=display_status,
            warning_message=warning_message,
            face_count=face_count,
            faces=faces,
            metrics=metrics,
        )
 
    def close(self):
        self._detector.close()
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
 
 
# =====================================================================
# 9. Rendering helpers (for standalone demo / debugging only)
# =====================================================================
 
def _blend_rect(img: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int], color: Tuple[int, int, int], alpha: float):
    """Alpha-blend a filled rectangle onto img in place (translucent panel)."""
    x1, y1 = pt1
    x2, y2 = pt2
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)
    if x2 <= x1 or y2 <= y1:
        return
    roi = img[y1:y2, x1:x2]
    overlay = np.full_like(roi, color, dtype=np.uint8)
    cv2.addWeighted(overlay, alpha, roi, 1 - alpha, 0, dst=roi)
 
 
def _put_text(img, text, org, scale, color, thickness, shadow=True):
    if shadow:
        cv2.putText(img, text, (org[0] + 1, org[1] + 1), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 1, cv2.LINE_AA)
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)
 
 
def draw_overlay(frame_bgr: np.ndarray, result: FrameAnalysisResult, fps: float = 0.0) -> np.ndarray:
    """Renders a clean, professional HUD: translucent top header with a
    colored status pill + face/FPS counters, a thin face bounding box,
    and -- only while an alert is active -- a bottom warning banner with
    an icon and bold message."""
    annotated = frame_bgr.copy()
    h, w = annotated.shape[:2]
    status = result.confirmed_status
    color = STATUS_COLORS.get(status, (255, 255, 255))
    is_alert = status != SystemStatus.NORMAL and result.warning_message is not None
 
    # Face bounding box(es)
    for face in result.faces:
        x_min, y_min, x_max, y_max = face.bbox
        box_color = color if is_alert else (0, 200, 0)
        cv2.rectangle(annotated, (x_min, y_min), (x_max, y_max), box_color, 2, cv2.LINE_AA)
 
    # --- Header bar ---
    header_h = 46
    _blend_rect(annotated, (0, 0), (w, header_h), (18, 18, 18), 0.55)
 
    # Status pill (rounded rect via a filled rounded rectangle approximation)
    pill_text = status.value
    (tw, th), _ = cv2.getTextSize(pill_text, cv2.FONT_HERSHEY_SIMPLEX, 0.62, 2)
    pill_pad_x, pill_pad_y = 14, 8
    pill_x1, pill_y1 = 14, (header_h - th - 2 * pill_pad_y) // 2
    pill_x2, pill_y2 = pill_x1 + tw + 2 * pill_pad_x, pill_y1 + th + 2 * pill_pad_y
    cv2.rectangle(annotated, (pill_x1, pill_y1), (pill_x2, pill_y2), color, -1, cv2.LINE_AA)
    cv2.rectangle(annotated, (pill_x1, pill_y1), (pill_x2, pill_y2), (255, 255, 255), 1, cv2.LINE_AA)
    text_color = (255, 255, 255) if sum(color) < 480 else (20, 20, 20)
    cv2.putText(
        annotated, pill_text, (pill_x1 + pill_pad_x, pill_y2 - pill_pad_y - 3),
        cv2.FONT_HERSHEY_SIMPLEX, 0.62, text_color, 2, cv2.LINE_AA,
    )
 
    # Right-aligned face/FPS counters
    meta_text = f"Faces: {result.face_count}    FPS: {fps:.1f}"
    (mw, _), _ = cv2.getTextSize(meta_text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
    _put_text(annotated, meta_text, (w - mw - 16, header_h // 2 + 6), 0.55, (210, 210, 210), 1)
 
    # --- Bottom warning banner (only while actively alerting) ---
    if is_alert:
        banner_h = 54
        y1, y2 = h - banner_h, h
        _blend_rect(annotated, (0, y1), (w, y2), (18, 18, 18), 0.65)
        cv2.rectangle(annotated, (0, y1), (6, y2), color, -1)  # left accent bar
 
        icon = "!"
        icon_center = (34, (y1 + y2) // 2)
        cv2.circle(annotated, icon_center, 14, color, -1, cv2.LINE_AA)
        (iw, ih), _ = cv2.getTextSize(icon, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.putText(
            annotated, icon, (icon_center[0] - iw // 2, icon_center[1] + ih // 2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA,
        )
 
        _put_text(
            annotated, result.warning_message, (58, (y1 + y2) // 2 + 6),
            0.68, (255, 255, 255), 2,
        )
 
    return annotated
 
 
# =====================================================================
# 10. Standalone webcam demo
# =====================================================================
 
def run_webcam_demo(config: Optional[MonitorConfig] = None):
    """
    Runs the module against a live webcam feed and shows the annotated
    output. Press 'q' to quit. This is a thin demo harness -- in a real
    proctoring system, the frame-acquisition loop typically lives in a
    higher-level orchestrator that also drives the other CV modules.
    """
    cfg = config or MonitorConfig()
 
    def _on_status_change(status: SystemStatus, message: Optional[str]):
        if message:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Status resolved: {status.value}")
 
    cap = cv2.VideoCapture(cfg.camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cfg.frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg.frame_height)
 
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam. Check camera_index / permissions.")
 
    prev_time = time.time()
    fps = 0.0
 
    with FaceVisibilityMonitor(cfg, on_status_change=_on_status_change) as monitor:
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
 
                frame = cv2.flip(frame, 1)  # mirror for a natural selfie view
                result = monitor.analyze(frame)
 
                now = time.time()
                dt = now - prev_time
                prev_time = now
                if dt > 0:
                    fps = 0.9 * fps + 0.1 * (1.0 / dt)
 
                annotated = draw_overlay(frame, result, fps)
                cv2.imshow("Exam Proctoring - Face Visibility Monitor", annotated)
 
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
    run_webcam_demo()
 

"""
core/pose_detector.py
Handles webcam capture and MediaPipe Pose landmark detection.
"""

import cv2
import mediapipe as mp
import numpy as np
from utils.helpers import load_config
import logging

logger = logging.getLogger("intellifit")
if not logger.hasHandlers():
    handler = logging.FileHandler("intellifit.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

config = load_config()
APP = config["app_settings"]


class PoseDetector:
    """Wraps MediaPipe Pose for landmark detection on video frames."""

    def __init__(self, confidence: float = None):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        conf = confidence or APP["mediapipe_confidence"]
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=conf,
            min_tracking_confidence=conf,
        )
        self.landmarks = None
        self._last_results = None

    # ── Frame Processing ───────────────────────────────────────────────────────

    def process(
        self,
        frame: np.ndarray,
        draw: bool = True,
        line_color: tuple[int, int, int] | None = None,
        landmark_color: tuple[int, int, int] | None = None,
    ) -> tuple[np.ndarray, bool]:
        """
        Run pose estimation on a BGR frame.
        Returns (annotated_frame, landmarks_detected).
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self.pose.process(rgb)
        rgb.flags.writeable = True
        frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        self._last_results = results

        if results.pose_landmarks:
            self.landmarks = results.pose_landmarks.landmark
            if draw:
                self._draw_skeleton(frame, results, line_color, landmark_color)
            return frame, True

        self.landmarks = None
        return frame, False

    def _draw_skeleton(
        self,
        frame: np.ndarray,
        results,
        line_color: tuple[int, int, int] | None = None,
        landmark_color: tuple[int, int, int] | None = None,
        connections=None,
    ) -> None:
        """Draw pose skeleton on frame using manual OpenCV drawing to exclude face/eyes."""
        if not results.pose_landmarks:
            return

        h, w, _ = frame.shape
        landmarks_px = {}
        for idx, lm in enumerate(results.pose_landmarks.landmark):
            # Exclude face landmarks (0 to 10) entirely
            if idx < 11:
                continue
            if lm.visibility > 0.5:
                landmarks_px[idx] = (int(lm.x * w), int(lm.y * h))

        conn_list = connections or self.mp_pose.POSE_CONNECTIONS
        draw_color = line_color or (0, 255, 0)
        joint_color = landmark_color or (0, 255, 0)

        # Draw connection lines
        for start_idx, end_idx in conn_list:
            if start_idx in landmarks_px and end_idx in landmarks_px:
                cv2.line(frame, landmarks_px[start_idx], landmarks_px[end_idx], draw_color, 3, cv2.LINE_AA)

        # Draw joint circles for active connected landmarks
        active_joints = set()
        for start_idx, end_idx in conn_list:
            if start_idx >= 11 and end_idx >= 11:
                active_joints.add(start_idx)
                active_joints.add(end_idx)

        for idx in active_joints:
            if idx in landmarks_px:
                cv2.circle(frame, landmarks_px[idx], 5, joint_color, -1, cv2.LINE_AA)
                cv2.circle(frame, landmarks_px[idx], 7, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_skeleton(
        self,
        frame: np.ndarray,
        line_color: tuple[int, int, int] | None = None,
        landmark_color: tuple[int, int, int] | None = None,
        connections=None,
    ) -> None:
        """Draw the last detected skeleton with optional colors."""
        if self._last_results and self._last_results.pose_landmarks:
            self._draw_skeleton(
                frame,
                self._last_results,
                line_color,
                landmark_color,
                connections,
            )

    # ── Landmark Utilities ─────────────────────────────────────────────────────

    def get_landmark(self, index: int, min_visibility: float = 0.5) -> tuple[float, float] | None:
        """Return (x, y) of a landmark by index if visibility is high enough, or None."""
        if self.landmarks is None:
            return None
        lm = self.landmarks[index]
        if lm.visibility < min_visibility:
            return None
        return lm.x, lm.y

    def get_landmark_px(self, index: int, w: int, h: int) -> tuple[int, int] | None:
        """Return pixel coordinates of a landmark."""
        coords = self.get_landmark(index)
        if coords is None:
            return None
        return int(coords[0] * w), int(coords[1] * h)

    def calculate_angle(self, a: int, b: int, c: int) -> float | None:
        """
        Calculate the angle (degrees) at landmark b, formed by a–b–c.
        Returns None if any landmark is missing or has low visibility.
        """
        pa = self.get_landmark(a)
        pb = self.get_landmark(b)
        pc = self.get_landmark(c)
        if None in (pa, pb, pc):
            logger.debug(f"calculate_angle({a},{b},{c}) returned None due to missing or low-visibility landmarks.")
            return None
        return _angle_between(pa, pb, pc)

    def close(self):
        self.pose.close()


# ── Math Helpers ───────────────────────────────────────────────────────────────

def _angle_between(a: tuple, b: tuple, c: tuple) -> float:
    """Compute angle at point b using vector math."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


# ── Webcam Context Manager ─────────────────────────────────────────────────────

class Webcam:
    """Context manager for OpenCV webcam access."""

    def __init__(self, index: int = 0):
        self.index = index
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, APP["webcam_width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, APP["webcam_height"])
        if not self.cap.isOpened():
            logger.error(f"Could not open webcam at index {self.index}.")
            raise RuntimeError("Could not open webcam. Check that it is connected.")
        logger.info(f"Webcam successfully opened at index {self.index}.")
        return self.cap

    def __exit__(self, *_):
        if self.cap:
            self.cap.release()

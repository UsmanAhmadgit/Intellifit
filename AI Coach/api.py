"""HTTP API for browser-based IntelliFit workout sessions."""

from __future__ import annotations

import base64
import os
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# The existing modules use imports relative to the intellifit directory.
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

from core.exercise_engine import EXERCISES, ExerciseEngine  # noqa: E402
from core.pose_detector import PoseDetector  # noqa: E402
from database import db_manager  # noqa: E402


app = FastAPI(title="IntelliFit CV API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionStart(BaseModel):
    exercise: str = Field(..., pattern="^(bicep_curl|squat)$")
    target_reps: int = Field(default=12, ge=1, le=100)


@dataclass
class WorkoutSession:
    exercise: str
    target_reps: int
    engine: ExerciseEngine
    detector: PoseDetector
    started_at: float
    lock: threading.Lock


sessions: dict[str, WorkoutSession] = {}


@app.on_event("startup")
def startup() -> None:
    db_manager.init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "intellifit-cv"}


@app.get("/api/exercises")
def exercises() -> list[dict[str, Any]]:
    return [
        {
            "key": key,
            "name": value["display_name"],
            "target_reps": value["target_reps"],
        }
        for key, value in EXERCISES.items()
    ]


@app.post("/api/sessions")
def start_session(request: SessionStart) -> dict[str, Any]:
    if request.exercise not in EXERCISES:
        raise HTTPException(status_code=400, detail="Unsupported exercise")

    session_id = str(uuid.uuid4())
    sessions[session_id] = WorkoutSession(
        exercise=request.exercise,
        target_reps=request.target_reps,
        engine=ExerciseEngine(request.exercise),
        detector=PoseDetector(),
        started_at=time.time(),
        lock=threading.Lock(),
    )
    return {"session_id": session_id, "exercise": request.exercise, "target_reps": request.target_reps}


@app.post("/api/sessions/{session_id}/frames")
async def process_frame(session_id: str, frame: UploadFile = File(...)) -> dict[str, Any]:
    session = _get_session(session_id)
    image = await frame.read()
    decoded = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), cv2.IMREAD_COLOR)
    if decoded is None:
        raise HTTPException(status_code=400, detail="Invalid image frame")

    with session.lock:
        annotated, detected = session.detector.process(decoded, draw=False)
        rep_result = _update_engine(session, detected)
        if detected:
            color = (0, 230, 118) if not session.engine.last_issues else (255, 171, 0)
            session.detector.draw_skeleton(
                annotated,
                line_color=color,
                landmark_color=color,
                connections=_POSE_CONNECTIONS,
            )
        ok, encoded = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 78])
        if not ok:
            raise HTTPException(status_code=500, detail="Could not encode annotated frame")

        feedback = list(session.engine.last_issues)
        response = _session_payload(session, detected, feedback)
        response["frame"] = base64.b64encode(encoded).decode("ascii")
        response["rep_event"] = rep_result is not None
        return response


@app.post("/api/sessions/{session_id}/stop")
def stop_session(session_id: str) -> dict[str, Any]:
    session = _get_session(session_id)
    with session.lock:
        summary = session.engine.summary()
        duration = max(0, int(time.time() - session.started_at))
        if session.engine.attempted_reps:
            db_manager.save_session(
                exercise=session.exercise,
                reps=summary["reps"],
                good_reps=summary["good_reps"],
                accuracy=summary["posture_accuracy"],
                duration_s=duration,
            )
            db_manager.update_streak(summary["reps"])
        summary["duration"] = duration
        summary["target_reps"] = session.target_reps
        session.detector.close()
        sessions.pop(session_id, None)
        return summary


@app.get("/api/analytics")
def analytics() -> dict[str, Any]:
    return {"sessions": db_manager.get_sessions(limit=100), "streak": db_manager.get_streak()}


def _get_session(session_id: str) -> WorkoutSession:
    session = sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Workout session not found")
    return session


def _update_engine(session: WorkoutSession, detected: bool):
    detector = session.detector
    engine = session.engine
    if not detected or engine.stage == "set_complete":
        return None

    if session.exercise == "bicep_curl":
        left = detector.calculate_angle(11, 13, 15)
        right = detector.calculate_angle(12, 14, 16)
        angle = right if right is not None and (left is None or abs(180 - right) > abs(180 - left)) else left
        extra = {}
    else:
        left = detector.calculate_angle(23, 25, 27)
        right = detector.calculate_angle(24, 26, 28)
        angles = [angle for angle in (left, right) if angle is not None]
        angle = sum(angles) / len(angles) if angles else None
        torso = [detector.calculate_angle(11, 23, 25), detector.calculate_angle(12, 24, 26)]
        torso_values = [value for value in torso if value is not None]
        alignment = []
        for hip, knee in ((23, 25), (24, 26)):
            hip_point = detector.get_landmark(hip)
            knee_point = detector.get_landmark(knee)
            if hip_point and knee_point:
                alignment.append(np.degrees(np.arctan2(abs(knee_point[0] - hip_point[0]), abs(knee_point[1] - hip_point[1]) + 1e-6)))
        extra = {
            "torso_angle": sum(torso_values) / len(torso_values) if torso_values else 90.0,
            "knee_alignment": sum(alignment) / len(alignment) if alignment else 0.0,
        }

    return engine.update(angle, **extra) if angle is not None else None


def _session_payload(session: WorkoutSession, detected: bool, feedback: list[str]) -> dict[str, Any]:
    engine = session.engine
    return {
        "detected": detected,
        "reps": engine.rep_count,
        "attempted_reps": engine.attempted_reps,
        "accuracy": engine.posture_accuracy,
        "stage": engine.stage or engine.frame_stage or "ready",
        "feedback": feedback,
        "target_reps": session.target_reps,
        "complete": engine.rep_count >= session.target_reps,
    }


_POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
    (11, 23), (12, 24), (23, 24), (23, 25), (25, 27),
    (24, 26), (26, 28),
]
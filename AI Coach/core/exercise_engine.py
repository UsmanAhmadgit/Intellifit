"""
core/exercise_engine.py
State machine for rep counting and posture evaluation per exercise.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from utils.helpers import load_config
import logging

logger = logging.getLogger("intellifit")
if not logger.hasHandlers():
    handler = logging.FileHandler("intellifit.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

config = load_config()
EXERCISES = config["exercises"]

def _eval_rule(rule: dict, ctx: dict) -> bool:
    """Safely evaluate a posture rule against the current context."""
    check = rule.get("check")
    if not isinstance(check, dict):
        return False
    
    val = ctx.get(check["variable"])
    if val is None:
        return False
        
    op = check["operator"]
    thr = check["threshold"]
    
    if op == "<": return val < thr
    if op == ">": return val > thr
    if op == "<=": return val <= thr
    if op == ">=": return val >= thr
    if op == "==": return val == thr
    
    return False


@dataclass
class RepResult:
    """Outcome of completing one repetition."""
    rep_number: int
    posture_ok: bool
    feedback: list[str] = field(default_factory=list)


class ExerciseEngine:
    """
    Tracks exercise state (up/down), counts reps, and evaluates posture.
    One instance per exercise session.
    """

    def __init__(self, exercise_name: str):
        if exercise_name not in EXERCISES:
            raise ValueError(f"Unknown exercise: {exercise_name}. "
                             f"Available: {list(EXERCISES.keys())}")
        self.name = exercise_name
        self.cfg = EXERCISES[exercise_name]
        self.stage: str | None = None   # "up" | "down" | None
        self.frame_stage: str | None = None
        self.ready: bool = False
        self.ready_frames: int = 0
        self.ready_frames_needed: int = int(self.cfg.get("ready_frames", 6))
        self.rep_count: int = 0
        self.good_reps: int = 0
        self.attempted_reps: int = 0
        self.session_feedback: list[str] = []
        self._pending_issues: list[str] = []
        self.last_issues: list[str] = []

        # EMA Smoothing variables
        self.smoothed_primary: float | None = None
        self.smoothed_extras: dict[str, float] = {}

        # Rep-level statistics tracking
        self.rep_min_angle: float = 180.0
        self.rep_max_angle: float = 0.0
        self.peak_extra_angles: dict[str, float] = {}

    # ── Main Update ────────────────────────────────────────────────────────────

    def update(self, primary_angle: float, **extra_angles) -> RepResult | None:
        """
        Feed the current joint angle into the state machine.
        Returns a RepResult when a rep completes, otherwise None.

        extra_angles: additional named angles (e.g. torso_angle=72) used
                      by posture rules that reference them.
        """
        # 1. Apply Exponential Moving Average (EMA) smoothing to filter out camera noise / jitter
        alpha = 0.35
        if self.smoothed_primary is None:
            self.smoothed_primary = primary_angle
            self.smoothed_extras = {k: float(v) for k, v in extra_angles.items()}
        else:
            self.smoothed_primary = alpha * primary_angle + (1.0 - alpha) * self.smoothed_primary
            for k, v in extra_angles.items():
                self.smoothed_extras[k] = alpha * float(v) + (1.0 - alpha) * self.smoothed_extras.get(k, float(v))

        primary_angle = self.smoothed_primary
        extra_angles = self.smoothed_extras

        # Track min/max during active phase
        if self.ready:
            self.rep_min_angle = min(self.rep_min_angle, primary_angle)
            self.rep_max_angle = max(self.rep_max_angle, primary_angle)
            # Capture extra angles at the peak of the motion (minimum primary angle / deepest contraction)
            if primary_angle <= self.rep_min_angle:
                self.peak_extra_angles = {k: v for k, v in extra_angles.items()}

        down_cfg = self.cfg["stages"]["down"]
        up_cfg = self.cfg["stages"]["up"]

        # Detect real-time frame posture issues (caving knees, forward lean)
        issues = self._check_posture(primary_angle, **extra_angles)
        self.last_issues = issues
        self.frame_stage = self._frame_stage(primary_angle)

        # Require a stable, perfect start position before counting reps
        if not self.ready:
            if self.frame_stage == "down" and not issues:
                self.ready_frames += 1
            else:
                self.ready_frames = 0
            if self.ready_frames >= self.ready_frames_needed:
                self.ready = True
                self.stage = "down"
                self.rep_min_angle = primary_angle
                self.rep_max_angle = primary_angle
                self.peak_extra_angles = {k: v for k, v in extra_angles.items()}
            return None

        # Accumulate real-time posture issues during the rep
        if issues:
            for issue in issues:
                if issue not in self._pending_issues:
                    self._pending_issues.append(issue)

        # State transitions
        if down_cfg["angle_min"] <= primary_angle <= down_cfg["angle_max"]:
            self.stage = "down"

        if up_cfg["angle_min"] <= primary_angle <= up_cfg["angle_max"]:
            if self.stage == "down":
                # Rep completed
                self.attempted_reps += 1
                
                # Check complete rep posture including range limits (incomplete extension/shallow squat)
                rep_issues = self._check_rep_posture()
                
                # Combine frame-level and rep-level issues
                all_issues = list(set(self._pending_issues + rep_issues))
                posture_ok = len(all_issues) == 0
                if posture_ok:
                    self.rep_count += 1
                    self.good_reps += 1
                result = RepResult(
                    rep_number=self.rep_count,
                    posture_ok=posture_ok,
                    feedback=all_issues,
                )
                self.session_feedback.extend(all_issues)
                self.last_issues = rep_issues  # Highlight final rep issues on skeleton
                
                # Reset for next rep
                self._pending_issues = []
                self.rep_min_angle = primary_angle
                self.rep_max_angle = primary_angle
                self.peak_extra_angles = {k: v for k, v in extra_angles.items()}
                
                self.stage = "up"
                return result
            self.stage = "up"

        return None

    # ── Posture Evaluation ─────────────────────────────────────────────────────

    def _check_posture(self, primary_angle: float, **extra_angles) -> list[str]:
        """Frame-level check for real-time posture feedback (skeleton color)."""
        issues = []
        angle_ctx = {"primary_angle": primary_angle, **extra_angles}
        frame_stage = self._frame_stage(primary_angle)

        for rule in self.cfg.get("posture_rules", []):
            check_expr = rule["check"]
            
            # Skip range completion limits on frame-level (evaluated at rep completion)
            if isinstance(check_expr, dict):
                var_name = check_expr.get("variable", "")
                if var_name in ("down_angle", "up_angle"):
                    continue
            else:
                if "down_angle" in check_expr or "up_angle" in check_expr:
                    continue

            try:
                when = rule.get("when")
                if when:
                    allowed = [when] if isinstance(when, str) else list(when)
                    if frame_stage not in allowed:
                        continue
                # Map generic names used in JSON to actual values
                local_ctx = {
                    "down_angle": primary_angle,
                    "up_angle": primary_angle,
                    "stage": frame_stage,
                    **angle_ctx,
                }
                if _eval_rule(rule, local_ctx):
                    issues.append(rule["feedback"])
            except Exception as e:
                logger.warning(f"Rule eval failed for rule {rule.get('id')}: {e}")

        return issues

    def _check_rep_posture(self) -> list[str]:
        """Evaluate range limits and final posture rules upon rep completion."""
        issues = []

        if self.name == "bicep_curl":
            down_angle = self.rep_max_angle  # Straight arm extension peak
            up_angle = self.rep_min_angle    # Curled arm contraction peak
        elif self.name == "squat":
            down_angle = self.rep_min_angle  # Knee angle at lowest squat depth
            up_angle = self.rep_max_angle    # Knee angle when fully stood up
        else:
            down_angle = self.rep_max_angle
            up_angle = self.rep_min_angle

        rep_ctx = {
            "down_angle": down_angle,
            "up_angle": up_angle,
            "primary_angle": down_angle,
            **self.peak_extra_angles
        }

        for rule in self.cfg.get("posture_rules", []):
            try:
                local_ctx = {
                    "down_angle": down_angle,
                    "up_angle": up_angle,
                    "stage": rule.get("when"),
                    **rep_ctx
                }
                if _eval_rule(rule, local_ctx):
                    issues.append(rule["feedback"])
            except Exception as e:
                logger.warning(f"Rule eval failed for rule {rule.get('id')}: {e}")

        return issues

    # ── Stats ──────────────────────────────────────────────────────────────────

    @property
    def posture_accuracy(self) -> float:
        """Percentage of good reps out of total reps."""
        if self.attempted_reps == 0:
            return 0.0
        return round((self.rep_count / self.attempted_reps) * 100, 1)

    @property
    def target_reps(self) -> int:
        return self.cfg.get("target_reps", 10)

    def summary(self) -> dict:
        return {
            "exercise": self.cfg["display_name"],
            "reps": self.rep_count,
            "good_reps": self.good_reps,
            "attempted_reps": self.attempted_reps,
            "posture_accuracy": self.posture_accuracy,
            "feedback_given": self.session_feedback,
        }

    def reset(self):
        self.stage = None
        self.frame_stage = None
        self.ready = False
        self.ready_frames = 0
        self.rep_count = 0
        self.good_reps = 0
        self.attempted_reps = 0
        self.session_feedback = []
        self._pending_issues = []
        self.last_issues = []
        self.smoothed_primary = None
        self.smoothed_extras = {}
        self.rep_min_angle = 180.0
        self.rep_max_angle = 0.0
        self.peak_extra_angles = {}

    def _frame_stage(self, primary_angle: float) -> str | None:
        down_cfg = self.cfg["stages"]["down"]
        up_cfg = self.cfg["stages"]["up"]
        if down_cfg["angle_min"] <= primary_angle <= down_cfg["angle_max"]:
            return "down"
        if up_cfg["angle_min"] <= primary_angle <= up_cfg["angle_max"]:
            return "up"
        return None

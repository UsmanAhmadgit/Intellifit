"""
gamification/badges.py
Checks earned badges after each session and returns new awards.
"""

from database import db_manager
from utils.helpers import load_config

config = load_config()
BADGE_DEFS = config["gamification"]["badges"]
MILESTONES = config["gamification"]["milestones"]


def check_and_award_badges(streak: dict, total_reps: int,
                            session_accuracy: float) -> list[dict]:
    """
    Evaluate all badge conditions and award any newly earned badges.
    Returns a list of newly awarded badge info dicts.
    """
    newly_earned = []
    earned = db_manager.get_earned_badges()

    candidates = {
        "first_workout":  streak["total_workouts"] >= 1,
        "streak_3":       streak["current_streak"] >= 3,
        "streak_7":       streak["current_streak"] >= 7,
        "streak_30":      streak["current_streak"] >= 30,
        "reps_100":       total_reps >= 100,
        "reps_500":       total_reps >= 500,
        "perfect_form":   session_accuracy >= 90.0,
    }

    for badge_id, condition in candidates.items():
        if condition and badge_id not in earned:
            awarded = db_manager.award_badge(badge_id)
            if awarded:
                newly_earned.append({
                    "id": badge_id,
                    **BADGE_DEFS[badge_id],
                })

    return newly_earned


def get_all_badges() -> dict:
    """Return all badge definitions with earned status."""
    earned = set(db_manager.get_earned_badges())
    result = {}
    for badge_id, info in BADGE_DEFS.items():
        result[badge_id] = {**info, "earned": badge_id in earned}
    return result

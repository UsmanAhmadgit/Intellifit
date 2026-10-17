"""
utils/helpers.py
JSON config loading and CSV export utilities.
"""

import json
import csv
import os
from datetime import datetime

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "exercises.json"
)
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "exports")


def load_config() -> dict:
    """Load and return the exercises.json configuration."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def export_sessions_csv(sessions: list[dict]) -> str:
    """
    Write session records to a timestamped CSV file in /exports.
    Returns the file path.
    """
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(EXPORTS_DIR, f"workout_history_{timestamp}.csv")

    if not sessions:
        return ""

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sessions[0].keys())
        writer.writeheader()
        writer.writerows(sessions)

    return path

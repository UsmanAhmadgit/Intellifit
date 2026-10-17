"""
database/db_manager.py
SQLite database operations for workout sessions, streaks, and badges.
"""

import sqlite3
import os
from datetime import date, datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "intellifit.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            exercise    TEXT NOT NULL,
            reps        INTEGER DEFAULT 0,
            good_reps   INTEGER DEFAULT 0,
            accuracy    REAL DEFAULT 0.0,
            duration_s  INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS streaks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            last_workout    TEXT,
            current_streak  INTEGER DEFAULT 0,
            longest_streak  INTEGER DEFAULT 0,
            total_workouts  INTEGER DEFAULT 0,
            total_reps      INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS badges (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            badge_id    TEXT UNIQUE NOT NULL,
            earned_at   TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)
        # Ensure one streak row exists
        conn.execute("INSERT OR IGNORE INTO streaks (id) VALUES (1)")
        conn.commit()


# ── Session Operations ─────────────────────────────────────────────────────────

def save_session(exercise: str, reps: int, good_reps: int,
                 accuracy: float, duration_s: int) -> int:
    """Insert a completed workout session. Returns the new row id."""
    today = date.today().isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (date, exercise, reps, good_reps, accuracy, duration_s) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (today, exercise, reps, good_reps, accuracy, duration_s),
        )
        conn.commit()
        return cur.lastrowid


def get_sessions(limit: int = 50) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_sessions_by_date_range(start: str, end: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE date BETWEEN ? AND ? ORDER BY date",
            (start, end),
        ).fetchall()
    return [dict(r) for r in rows]


# ── Streak Operations ──────────────────────────────────────────────────────────

def update_streak(reps_added: int) -> dict:
    """Update streak after a workout. Returns updated streak info."""
    today = date.today().isoformat()
    with get_connection() as conn:
        row = dict(conn.execute("SELECT * FROM streaks WHERE id=1").fetchone())
        last = row["last_workout"]
        current = row["current_streak"]
        longest = row["longest_streak"]
        total_workouts = row["total_workouts"] + 1
        total_reps = row["total_reps"] + reps_added

        if last == today:
            pass  # Already worked out today — no streak change
        elif last == _yesterday():
            current += 1
        else:
            current = 1  # Streak broken — reset

        longest = max(longest, current)

        conn.execute(
            "UPDATE streaks SET last_workout=?, current_streak=?, longest_streak=?, "
            "total_workouts=?, total_reps=? WHERE id=1",
            (today, current, longest, total_workouts, total_reps),
        )
        conn.commit()
    return get_streak()


def get_streak() -> dict:
    with get_connection() as conn:
        return dict(conn.execute("SELECT * FROM streaks WHERE id=1").fetchone())


# ── Badge Operations ───────────────────────────────────────────────────────────

def award_badge(badge_id: str) -> bool:
    """Award a badge. Returns True if newly awarded, False if already had it."""
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO badges (badge_id) VALUES (?)", (badge_id,))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_earned_badges() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute("SELECT badge_id FROM badges").fetchall()
    return [r["badge_id"] for r in rows]


# ── Helpers ────────────────────────────────────────────────────────────────────

def _yesterday() -> str:
    from datetime import timedelta
    return (date.today() - timedelta(days=1)).isoformat()

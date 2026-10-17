"""
analytics/charts.py
Plotly chart generators for the analytics page — dark themed.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Shared Dark Theme Layout ──────────────────────────────────────────────────
_DARK_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(17,25,40,0.5)",
    font=dict(family="Inter, sans-serif", color="#c8d6e5", size=12),
    title_font=dict(size=15, color="#ffffff", family="Inter, sans-serif"),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#8899aa"),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=10, color="#8899aa"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=10, color="#8899aa"),
    ),
)


def _apply_theme(fig):
    """Apply the shared dark theme to a Plotly figure."""
    fig.update_layout(**_DARK_LAYOUT)
    return fig


def build_reps_over_time(sessions: list[dict]):
    """Line chart — total reps per day."""
    if not sessions:
        return None
    df = pd.DataFrame(sessions)
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby("date")["reps"].sum().reset_index()
    fig = px.line(
        daily, x="date", y="reps",
        title="📈 Reps Over Time",
        labels={"date": "", "reps": "Total Reps"},
        markers=True,
        color_discrete_sequence=["#00d4ff"],
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8, line=dict(width=2, color="#0e1117")),
        fill="tozeroy",
        fillcolor="rgba(0, 212, 255, 0.08)",
    )
    return _apply_theme(fig)


def build_accuracy_chart(sessions: list[dict]):
    """Bar chart — posture accuracy per session."""
    if not sessions:
        return None
    df = pd.DataFrame(sessions)
    df["session_label"] = df["date"] + " #" + df["id"].astype(str)
    fig = px.bar(
        df.tail(20), x="session_label", y="accuracy",
        title="🎯 Posture Accuracy per Session",
        labels={"session_label": "", "accuracy": "Accuracy (%)"},
        color="accuracy",
        color_continuous_scale=["#ff1744", "#ffab00", "#00e676"],
        range_color=[0, 100],
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        xaxis_tickangle=-45,
        coloraxis_colorbar=dict(
            title="",
            tickfont=dict(size=10, color="#8899aa"),
            len=0.6,
        ),
    )
    return _apply_theme(fig)


def build_exercise_split(sessions: list[dict]):
    """Donut chart — workout distribution by exercise type."""
    if not sessions:
        return None
    df = pd.DataFrame(sessions)
    split = df.groupby("exercise")["reps"].sum().reset_index()
    fig = px.pie(
        split, names="exercise", values="reps",
        title="🏋️ Exercise Split",
        color_discrete_sequence=["#00d4ff", "#7c4dff", "#00e676", "#ffab00", "#ff1744"],
        hole=0.45,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont_size=12,
        marker=dict(line=dict(color="#0e1117", width=2)),
    )
    return _apply_theme(fig)


def build_weekly_heatmap(sessions: list[dict]):
    """Heatmap of workout days — shows consistency."""
    if not sessions:
        return None
    df = pd.DataFrame(sessions)
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week.astype(str)
    df["day"] = df["date"].dt.day_name()

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = df.pivot_table(index="day", columns="week", values="reps", aggfunc="sum", fill_value=0)
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])

    fig = px.imshow(
        pivot,
        title="🗓️ Weekly Workout Heatmap",
        labels={"x": "Week", "y": "", "color": "Reps"},
        color_continuous_scale=["rgba(0,212,255,0.05)", "#00d4ff", "#7c4dff"],
        aspect="auto",
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="",
            tickfont=dict(size=10, color="#8899aa"),
            len=0.6,
        ),
    )
    return _apply_theme(fig)

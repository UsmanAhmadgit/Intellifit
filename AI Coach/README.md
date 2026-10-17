# 💪 INTELLIFIT
### AI-Powered Fitness Coach

IntelliFit is a browser-based workout platform that uses a webcam, MediaPipe pose landmarks, and angle-based movement analysis to count repetitions and provide real-time posture feedback without wearable devices.

## The Problem

People exercising at home may not have equipment, a personal coach, or a reliable way to track repetitions and maintain safe form. IntelliFit brings guided workouts and movement feedback into a single home-training experience.

## The Approach

The app combines a responsive workout dashboard with a Python computer-vision service. The browser captures camera frames, the FastAPI backend analyzes body landmarks, and the exercise engine evaluates movement stages, repetitions, range of motion, and posture quality. Completed sessions are stored in SQLite for progress and streak tracking.

## Current Capabilities

- Guided exercise library with demonstration media and set timers
- Browser camera-based rep counting for **Bicep Curl** and **Squat**
- Real-time posture feedback for arm extension, squat depth, torso angle, and knee alignment
- Annotated pose frames with skeleton color changes based on form quality
- Target repetitions, attempted repetitions, clean repetitions, and accuracy scoring
- SQLite session history and workout streak tracking
- Frontend views for AI Coach, Community, Settings, and Analytics

The dashboard currently contains additional guided exercises, while live computer-vision rules are implemented for the two exercises above. Community, Settings, and the visual Analytics page are currently frontend experiences; their backend persistence and real-data connections can be extended next.

---

## 👥 Group Members
| Name | Roll No | Module |
|------|---------|--------|
| Ammar Tariq | SP24-BAI-027 | UI & Feedback System |
| Usman Ahmad | SP24-BAI-048 | Computer Vision & Exercise Detection |
| Faizan Azhar | SP24-BAI-030 | Database, Analytics & Gamification |

---

## 🗂️ Project Structure

```
intellifit/
├── api.py                      ← FastAPI CV service
├── requirements.txt            ← All dependencies
├── .gitignore
│
├── config/
│   └── exercises.json          ← Angle thresholds, posture rules, badges
│
├── core/
│   ├── pose_detector.py        ← OpenCV + MediaPipe landmark detection
│   └── exercise_engine.py      ← Rep counting + posture evaluation
│
├── feedback/
│   └── voice_coach.py          ← gTTS + playsound audio feedback (async)
│
├── database/
│   └── db_manager.py           ← SQLite CRUD (sessions, streaks, badges)
│
├── analytics/
│   └── charts.py               ← Plotly/Matplotlib chart generators
│
├── gamification/
│   └── badges.py               ← Badge and milestone logic
│
├── utils/
│   └── helpers.py              ← JSON config loader, CSV exporter
│
├── data/
│   ├── intellifit.db            ← Auto-created SQLite DB
│   └── exports/                 ← CSV workout exports (auto-created)
└── assets/                     ← Icons, images (optional)
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/intellifit.git
cd intellifit
```

### Step 2 — Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python dependencies
```bash
python -m pip install -r intellifit/requirements.txt
```

> ⚠️ **MediaPipe Note:** MediaPipe requires Python 3.8–3.11.
> If you have Python 3.12+, use Python 3.11 for your virtual environment.

### Step 4 — Verify webcam access
Make sure your webcam is connected and not blocked by another application.

### Step 5 — Start the CV backend
```bash
uvicorn intellifit.api:app --reload --host 127.0.0.1 --port 8000
```

### Step 6 — Start the frontend in a second terminal
From the project root:
```bash
npm install
npm run dev
```

Open `http://localhost:3000`, select **Login**, and use the **AI Form Coach** panel.

---

## 🎯 How to Use

1. Open the frontend and go to the dashboard.
2. Select **Bicep Curl** or **Squat** in **AI Form Coach**.
3. Click **Start AI Coach** and allow camera access.
4. Keep your full body visible and follow the live feedback.
5. Click **Stop & Save** to persist the session in SQLite.

---

## 🔧 Configuration

All exercise settings live in `config/exercises.json`:

- **Angle thresholds** — when a joint angle is "up" vs "down"
- **Posture rules** — conditions that trigger feedback messages
- **Badge definitions** — unlock criteria and display info
- **App settings** — webcam resolution, MediaPipe confidence, colors

Modify this file to add new exercises or tune existing ones — **no code change needed.**

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| HTML, CSS, JavaScript | Browser dashboard and navigation |
| FastAPI + Uvicorn | Browser CV API |
| OpenCV | Webcam capture & frame processing |
| MediaPipe Pose | 33-point body landmark detection |
| NumPy | Vector math for angle calculation |
| Pandas | Workout data processing |
| Plotly | Interactive analytics charts |
| Matplotlib | Static chart generation |
| SQLite (sqlite3) | Local database storage |
| gTTS / playsound | Optional backend voice-coaching module |
| Git & GitHub | Version control |

---

## 📋 Features Checklist

- [x] Real-time pose detection (33 landmarks)
- [x] Configured CV exercise analysis (Bicep Curl, Squat)
- [x] Automatic rep counting via state machine
- [x] Posture correction feedback
- [x] Optional voice-coaching module (gTTS)
- [x] Workout analytics API and frontend analytics view
- [x] Streak tracking
- [x] Achievement badges
- [x] SQLite data persistence
- [x] CSV export
- [x] JSON configuration

---

## 🐛 Common Issues

**"Could not open webcam"**
→ Close any other app using the webcam (Zoom, Teams, etc.)

**MediaPipe installation fails**
→ Ensure Python 3.8–3.11 is used: `python --version`

**No voice audio**
→ Check system audio settings. Voice uses `playsound` and is optional.

**API unavailable in the dashboard**
→ Start `uvicorn intellifit.api:app --reload --port 8000` in a second terminal.

---

## 📁 Git Workflow (Team)

```bash
# Initial setup (once)
git init
git remote add origin https://github.com/YOUR_USERNAME/intellifit.git

# Daily workflow
git pull origin main          # Get latest changes
git add .
git commit -m "feat: add squat detection"
git push origin main

# Branch per feature (recommended)
git checkout -b feature/analytics-dashboard
# ... work ...
git push origin feature/analytics-dashboard
# Open a Pull Request on GitHub
```

---

## 📜 License
This project is developed for academic purposes — BAI Fall 2024.

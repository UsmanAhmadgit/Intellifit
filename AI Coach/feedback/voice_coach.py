"""
feedback/voice_coach.py
Asynchronous voice feedback using gTTS + playsound.
Runs audio in a background thread and uses local caching to prevent network latency blocking.
"""

import threading
import os
import time
import hashlib
import logging
from gtts import gTTS

logger = logging.getLogger("intellifit")

try:
    from playsound import playsound
except Exception:
    playsound = None


def _play_with_system(path: str) -> None:
    os.system(
        f"mpg123 -q {path} 2>/dev/null || "
        f"afplay {path} 2>/dev/null || "
        f"aplay {path} 2>/dev/null"
    )


class VoiceCoach:
    """Text-to-speech coach that speaks feedback asynchronously."""

    def __init__(self, enabled: bool = True, lang: str = "en"):
        self.enabled = enabled
        self.lang = lang
        self._lock = threading.Lock()
        self._speaking = False
        
        # Audio caching
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".audio_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cooldown management
        self.last_played = {}
        self.cooldowns = {
            "good_rep": 3.0,
            "correction": 5.0,
            "milestone": 0.0
        }

    def _get_audio_path(self, message: str) -> str:
        h = hashlib.md5(message.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir, f"{h}.mp3")

    def _generate_audio(self, message: str, path: str):
        if not os.path.exists(path):
            try:
                tts = gTTS(text=message, lang=self.lang, slow=False)
                tts.save(path)
            except Exception as e:
                logger.error(f"TTS generation failed: {e}")

    def speak(self, message: str, msg_type: str = "correction") -> None:
        if not self.enabled:
            return
            
        now = time.time()
        
        # Check cooldown for this specific message type
        cooldown = self.cooldowns.get(msg_type, 2.0)
        if msg_type in self.last_played:
            if now - self.last_played[msg_type] < cooldown:
                return # Cooldown active
                
        # We also want to avoid spamming the exact same correction message repeatedly
        if msg_type == "correction":
            if message in self.last_played:
                if now - self.last_played[message] < self.cooldowns["correction"]:
                    return
            self.last_played[message] = now
            
        self.last_played[msg_type] = now
        
        # If currently speaking, drop the message
        if self._speaking:
            return
            
        thread = threading.Thread(target=self._speak_worker, args=(message,), daemon=True)
        thread.start()

    def _speak_worker(self, message: str) -> None:
        path = self._get_audio_path(message)
        self._generate_audio(message, path)
        
        if not os.path.exists(path):
            return
            
        with self._lock:
            self._speaking = True
            try:
                if playsound:
                    try:
                        playsound(path)
                    except Exception:
                        _play_with_system(path)
                else:
                    _play_with_system(path)
            except Exception as e:
                logger.error(f"[VoiceCoach] Playback Error: {e}")
            finally:
                self._speaking = False

    def good_rep(self, exercise: str = "") -> None:
        self.speak(f"Good {exercise} repetition! Keep it up.", msg_type="good_rep")

    def correction(self, message: str) -> None:
        self.speak(message, msg_type="correction")

    def milestone(self, reps: int) -> None:
        self.speak(f"Amazing! {reps} repetitions completed!", msg_type="milestone")

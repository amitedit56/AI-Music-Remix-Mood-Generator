import os
import io
import random
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def detect_mood(audio_bytes: bytes, filename: str = "") -> dict:
    """
    Detect mood by analysing real audio features (tempo, energy, brightness)
    using librosa. Falls back to filename-based hashing if librosa unavailable.
    Returns: { "success": True, "mood": "Happy", "confidence": 88.0, "tempo": 120 }
    """
    try:
        import librosa
        import numpy as np

        # Load audio (first 30 sec is enough for analysis — faster)
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=22050, duration=30)

        # ── Extract features ────────────────────────────────────────────────
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(np.asarray(tempo).item())

        rms = float(np.mean(librosa.feature.rms(y=y)))          # loudness/energy
        spectral_centroid = float(np.mean(
            librosa.feature.spectral_centroid(y=y, sr=sr)
        ))  # brightness — higher = brighter/sharper sound

        # ── Decide mood based on tempo + energy + brightness ───────────────
        if tempo > 120 and rms > 0.05:
            mood = "Energetic"
            confidence = 88.0
        elif tempo > 110 and spectral_centroid > 2000:
            mood = "Happy"
            confidence = 85.0
        elif tempo < 80 and rms < 0.04:
            mood = "Sad"
            confidence = 82.0
        elif tempo < 95 and spectral_centroid < 1800:
            mood = "Chill"
            confidence = 80.0
        elif rms > 0.06:
            mood = "Party"
            confidence = 84.0
        else:
            mood = "Romantic"
            confidence = 78.0

        return {
            "success"   : True,
            "mood"      : mood,
            "confidence": confidence,
            "tempo"     : round(tempo, 1),
            "energy"    : round(rms, 4)
        }

    except Exception as e:
        # Fallback: hash filename so result is consistent per-file but varies
        seed = sum(ord(c) for c in filename) if filename else len(audio_bytes)
        moods = ["Happy", "Sad", "Chill", "Energetic", "Romantic", "Party"]
        random.seed(seed)
        mood = random.choice(moods)

        return {
            "success"   : True,
            "mood"      : mood,
            "confidence": 75.0,
            "note"      : f"Fallback mode (librosa error: {str(e)[:50]})"
        }


def detect_mood_from_prompt(prompt: str, mood: str, genre: str) -> dict:
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type" : "application/json"
        }

        messages = [
            {
                "role": "system",
                "content": """You are a music mood analyzer. 
                Given a user's music description, mood, and genre — analyze and return a JSON response with:
                - detected_mood: one of (Happy, Sad, Chill, Energetic, Romantic, Party, Calm, Angry)
                - confidence: percentage 0-100
                - music_description: a detailed description for music generation (2-3 sentences)
                - suggested_instruments: list of 3-4 instruments that fit the mood
                Return ONLY valid JSON, no extra text."""
            },
            {
                "role": "user",
                "content": f"User prompt: '{prompt}'\nSelected mood: {mood}\nSelected genre: {genre}"
            }
        ]

        payload = {
            "model"      : "llama-3.3-70b-versatile",
            "messages"   : messages,
            "temperature": 0.7,
            "max_tokens" : 300
        }

        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            data    = response.json()
            content = data["choices"][0]["message"]["content"]

            import json
            import re
            content_clean = content.strip()
            if content_clean.startswith("```"):
                content_clean = content_clean.split("```")[1]
                if content_clean.startswith("json"):
                    content_clean = content_clean[4:]
            content_clean = content_clean.rstrip("```").strip()
            content_clean = re.sub(r'[\x00-\x1f\x7f]', ' ', content_clean)

            result = json.loads(content_clean, strict=False)

            return {
                "success"              : True,
                "mood"                 : result.get("detected_mood", mood),
                "confidence"           : result.get("confidence", 85),
                "music_description"    : result.get("music_description", ""),
                "suggested_instruments": result.get("suggested_instruments", [])
            }

        else:
            return {
                "success"   : False,
                "error"     : f"Groq API error: {response.status_code}"
            }

    except Exception as e:
        return {
            "success" : False,
            "error"   : str(e)
        }


def mood_to_genre(mood: str) -> str:
    mapping = {
        "Happy"     : "Pop",
        "Sad"       : "Lo-fi",
        "Angry"     : "Rock",
        "Neutral"   : "Jazz",
        "Fearful"   : "Classical",
        "Disgusted" : "EDM",
        "Surprised" : "EDM",
        "Calm"      : "Lo-fi",
        "Energetic" : "EDM",
        "Party"     : "EDM",
        "Romantic"  : "Jazz",
    }
    return mapping.get(mood, "Lo-fi")
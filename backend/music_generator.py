import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def build_prompt(mood: str, genre: str, user_prompt: str = "") -> str:
    mood_descriptions = {
        "Happy"     : "upbeat, bright melody, cheerful",
        "Sad"       : "melancholic, slow tempo, emotional",
        "Chill"     : "relaxed, soft beats, calm atmosphere",
        "Energetic" : "fast tempo, high energy, powerful",
        "Romantic"  : "warm, gentle melody, soft piano",
        "Party"     : "danceable, strong beat, fun",
        "Angry"     : "intense, heavy, aggressive rhythm",
        "Neutral"   : "smooth, balanced, flowing",
        "Calm"      : "peaceful, ambient, soothing",
    }
    base        = f"{mood.lower()} {genre.lower()} music"
    description = mood_descriptions.get(mood, "smooth and flowing")

    if user_prompt.strip():
        return f"{base}, {user_prompt.strip()}, {description}"
    return f"{base}, {description}"


def generate_music(mood: str, genre: str, user_prompt: str = "", duration: int = 10) -> dict:
    """
    Generate music description + remix tips using Groq AI
    Returns: { "success": True, "description": "...", "remix_tips": [...], "prompt_used": "..." }
    """
    prompt = build_prompt(mood, genre, user_prompt)

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type" : "application/json"
        }

        messages = [
            {
                "role": "system",
                "content": """You are an expert music producer and DJ. 
                When given a music style description, generate a detailed remix plan.
                Return ONLY valid JSON with these fields:
                - title: creative name for this remix (e.g. "Midnight Lo-fi Chill")
                - description: vivid 2-3 sentence description of how the music sounds
                - bpm: suggested BPM number (integer)
                - key: musical key (e.g. "C minor", "G major")
                - instruments: list of 4-5 instruments
                - effects: list of 3-4 audio effects to apply
                - remix_tips: list of 3 specific tips to remix this track
                - energy_level: Low / Medium / High
                No extra text, only JSON."""
            },
            {
                "role": "user",
                "content": f"Create a remix plan for: {prompt}"
            }
        ]

        payload = {
            "model"      : "llama-3.3-70b-versatile",
            "messages"   : messages,
            "temperature": 0.8,
            "max_tokens" : 500
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
            content_clean = content.strip()
            if content_clean.startswith("```"):
                content_clean = content_clean.split("```")[1]
                if content_clean.startswith("json"):
                    content_clean = content_clean[4:]
            content_clean = content_clean.rstrip("```").strip()

            # Remove invalid control characters (newlines/tabs inside strings)
            import re
            content_clean = re.sub(r'[\x00-\x1f\x7f]', ' ', content_clean)

            result = json.loads(content_clean, strict=False)

            return {
                "success"     : True,
                "title"       : result.get("title", f"{mood} {genre} Remix"),
                "description" : result.get("description", ""),
                "bpm"         : result.get("bpm", 120),
                "key"         : result.get("key", "C major"),
                "instruments" : result.get("instruments", []),
                "effects"     : result.get("effects", []),
                "remix_tips"  : result.get("remix_tips", []),
                "energy_level": result.get("energy_level", "Medium"),
                "prompt_used" : prompt
            }

        elif response.status_code == 401:
            return {
                "success" : False,
                "error"   : "Invalid Groq API key. Please check your .env file."
            }

        else:
            return {
                "success" : False,
                "error"   : f"Groq API error: {response.status_code}"
            }

    except Exception as e:
        return {
            "success" : False,
            "error"   : str(e)
        }
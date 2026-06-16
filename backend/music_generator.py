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
                - description: vivid 2-3 sentence PLAIN TEXT description of how the music sounds (no HTML, no markdown, no code, just natural language sentences)
                - bpm: suggested BPM number (integer)
                - key: musical key (e.g. "C minor", "G major")
                - instruments: list of 4-5 instrument names as plain text strings
                - effects: list of 3-4 audio effect names as plain text strings
                - remix_tips: list of 3 specific tips to remix this track, as plain text strings
                - energy_level: Low / Medium / High
                IMPORTANT: All text values must be plain natural language. Never include HTML tags, <div>, <span>, <p>, CSS, or any markup of any kind in any field.
                No extra text, only JSON."""
            },
            {
                "role": "user",
                "content": f"Create a remix plan for: {prompt}"
            }
        ]

        payload = {
            "model"          : "llama-3.3-70b-versatile",
            "messages"       : messages,
            "temperature"    : 0.7,
            "max_tokens"     : 500,
            "response_format": {"type": "json_object"}
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

            def clean_text(value, default=""):
                """Strip HTML/CSS/markdown markup; if too much was removed, use default instead"""
                if not isinstance(value, str):
                    return default
                original_len = len(value)
                cleaned = re.sub(r'<[^>]+>', '', value)
                cleaned = re.sub(r'\{[^}]*\}', '', cleaned)  # remove CSS-like {...} blocks
                cleaned = cleaned.replace('`', '').replace('"', "'")  # remove backticks, normalize quotes
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                # If more than 30% of the text was markup/CSS, it's unreliable — use default
                if original_len > 0 and len(cleaned) < original_len * 0.6:
                    return default
                return cleaned if cleaned else default

            def clean_list(items):
                """Clean each item in a list of strings"""
                if not isinstance(items, list):
                    return []
                return [clean_text(i) for i in items if isinstance(i, str) and clean_text(i)]

            return {
                "success"     : True,
                "title"       : clean_text(result.get("title"), f"{mood} {genre} Remix"),
                "description" : clean_text(result.get("description"), f"A {mood.lower()} {genre.lower()} remix tailored to your selected vibe."),
                "bpm"         : result.get("bpm", 120),
                "key"         : clean_text(result.get("key"), "C major"),
                "instruments" : clean_list(result.get("instruments", [])),
                "effects"     : clean_list(result.get("effects", [])),
                "remix_tips"  : clean_list(result.get("remix_tips", [])),
                "energy_level": clean_text(result.get("energy_level"), "Medium"),
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
import os
import io
from pydub import AudioSegment
from pydub.effects import normalize


def save_temp_audio(audio_bytes: bytes, filename: str, temp_dir: str = "temp_audio") -> str:
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    return file_path


def delete_temp_audio(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass


def get_file_info(audio_bytes: bytes, filename: str) -> dict:
    size_kb   = round(len(audio_bytes) / 1024, 1)
    size_mb   = round(len(audio_bytes) / (1024 * 1024), 2)
    extension = filename.split(".")[-1].upper()

    if extension == "WAV":
        estimated_duration = round(size_kb / 176, 1)
    else:
        estimated_duration = round(size_kb / 16, 1)

    return {
        "size_kb"            : size_kb,
        "size_mb"            : size_mb,
        "extension"          : extension,
        "estimated_duration" : estimated_duration
    }


def apply_mood_effects(audio_bytes: bytes, filename: str, mood: str, genre: str, prompt: str = "", quality: str = "High") -> dict:
    """
    Apply real audio effects based on mood and genre using pydub
    Returns: { "success": True, "audio_bytes": b"...", "effects_applied": [...] }
    """
    try:
        extension = filename.split(".")[-1].lower()

        # Load audio from bytes
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=extension)

        effects_applied = []

        # ── Mood-based effects ──────────────────────────────────────────────

        if mood == "Happy":
            # Speed up slightly + volume boost
            audio = audio.speedup(playback_speed=1.08)
            audio = audio + 3  # +3dB volume
            effects_applied.extend(["Speed boost +8%", "Volume +3dB"])

        elif mood == "Sad":
            # Slow down + reduce volume slightly
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * 0.92)
            }).set_frame_rate(audio.frame_rate)
            audio = audio - 2  # -2dB
            effects_applied.extend(["Slowed -8%", "Volume -2dB"])

        elif mood == "Chill":
            # Slight slowdown + bass boost
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * 0.95)
            }).set_frame_rate(audio.frame_rate)
            effects_applied.append("Slowed -5% for chill vibe")

        elif mood == "Energetic":
            # Speed up + volume boost
            audio = audio.speedup(playback_speed=1.12)
            audio = audio + 4
            effects_applied.extend(["Speed boost +12%", "Volume +4dB"])

        elif mood == "Romantic":
            # Slow + soften
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * 0.94)
            }).set_frame_rate(audio.frame_rate)
            audio = audio - 1
            effects_applied.extend(["Slowed -6%", "Softened -1dB"])

        elif mood == "Party":
            # Speed up + loud
            audio = audio.speedup(playback_speed=1.15)
            audio = audio + 5
            effects_applied.extend(["Speed boost +15%", "Volume +5dB"])

        # ── Prompt-based keyword effects ────────────────────────────────────
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ["fast", "energetic", "upbeat", "high energy", "powerful"]):
            audio = audio.speedup(playback_speed=1.06)
            effects_applied.append("Prompt keyword 'fast/energetic' → +6% speed")

        if any(word in prompt_lower for word in ["slow", "relax", "calm", "soft", "gentle", "mellow"]):
            audio = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate * 0.96)
            }).set_frame_rate(audio.frame_rate)
            effects_applied.append("Prompt keyword 'slow/calm' → -4% speed")

        if any(word in prompt_lower for word in ["bass", "deep", "heavy", "powerful drop"]):
            audio = audio + 4
            effects_applied.append("Prompt keyword 'bass/heavy' → +4dB bass boost")

        if any(word in prompt_lower for word in ["rain", "vinyl", "crackle", "lo-fi", "lofi", "cozy"]):
            audio = audio.set_frame_rate(22050).set_frame_rate(44100)
            effects_applied.append("Prompt keyword 'lo-fi/vinyl' → lo-fi texture")

        if any(word in prompt_lower for word in ["echo", "reverb", "night", "ambient", "dreamy"]):
            from pydub import effects as pydub_effects
            audio = audio.overlay(audio - 15, position=120)  # simple echo simulation
            effects_applied.append("Prompt keyword 'echo/ambient' → echo effect")

        # ── Genre-based effects ─────────────────────────────────────────────

        if genre == "Lo-fi":
            # Reduce sample rate for lo-fi feel
            audio = audio.set_frame_rate(22050).set_frame_rate(44100)
            effects_applied.append("Lo-fi filter applied")

        elif genre == "EDM":
            audio = audio + 3
            effects_applied.append("EDM volume boost")

        elif genre == "Classical":
            audio = audio - 2
            effects_applied.append("Classical softening")

        # ── Normalize at the end ────────────────────────────────────────────
        audio = normalize(audio)
        effects_applied.append("Normalized output")

        # ── Fade in / Fade out ──────────────────────────────────────────────
        audio = audio.fade_in(500).fade_out(1000)
        effects_applied.append("Fade in/out added")

        # ── Output Quality ───────────────────────────────────────────────────
        quality_settings = {
            "Standard": {"bitrate": "96k",  "frame_rate": 22050},
            "High"    : {"bitrate": "192k", "frame_rate": 44100},
            "Ultra"   : {"bitrate": "320k", "frame_rate": 48000},
        }
        q = quality_settings.get(quality, quality_settings["High"])

        audio = audio.set_frame_rate(q["frame_rate"])
        effects_applied.append(f"{quality} quality — {q['frame_rate']}Hz @ {q['bitrate']}")

        # ── Export to bytes ─────────────────────────────────────────────────
        output_buffer = io.BytesIO()
        audio.export(output_buffer, format="mp3", bitrate=q["bitrate"])
        output_bytes = output_buffer.getvalue()

        return {
            "success"        : True,
            "audio_bytes"    : output_bytes,
            "effects_applied": effects_applied,
            "format"         : "mp3",
            "bitrate"        : q["bitrate"],
            "sample_rate"    : q["frame_rate"]
        }

    except Exception as e:
        return {
            "success" : False,
            "error"   : str(e)
        }


def is_valid_audio(filename: str) -> bool:
    allowed = ["mp3", "wav"]
    ext = filename.split(".")[-1].lower()
    return ext in allowed
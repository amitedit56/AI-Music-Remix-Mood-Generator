import streamlit as st
import streamlit.components.v1 as components
import time
import sys
import os
import random
sys.path.append(os.path.dirname(__file__))
from backend.mood_detector import detect_mood, mood_to_genre
from backend.music_generator import generate_music
from backend.audio_utils import apply_mood_effects, get_file_info

st.set_page_config(
    page_title="StudioAI — Music Remix",
    page_icon="🎚️",
    layout="wide"
)

# ─── CSS ────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, .stApp {
    background: #080B14;
    font-family: 'Inter', sans-serif;
    color: #F1F5F9;
    color-scheme: dark;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0F1424; }
::-webkit-scrollbar-thumb { background: #7C3AED; border-radius: 2px; }

/* ── Page wrapper ── */
.block-container {
    max-width: 860px !important;
    padding: 3rem 2rem 4rem !important;
    margin: 0 auto;
}

/* ── Ambient glow ── */
.stApp::before {
    content: '';
    position: fixed;
    top: -200px; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 500px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.18) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 2rem 0 2.5rem;
    position: relative;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 999px;
    padding: 5px 16px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #A78BFA;
    margin-bottom: 1.4rem;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -0.03em;
    color: #F1F5F9;
    margin-bottom: 1rem;
}

.hero-title .accent-purple { color: #A78BFA; }
.hero-title .accent-cyan { color: #00D4FF; }

.hero-sub {
    font-size: 16px;
    color: #64748B;
    font-weight: 400;
    line-height: 1.6;
    max-width: 480px;
    margin: 0 auto;
}

/* ── Waveform decoration ── */
.waveform {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    height: 32px;
    margin: 1.8rem auto 0;
}

.waveform span {
    display: block;
    width: 3px;
    border-radius: 2px;
    background: linear-gradient(180deg, #7C3AED, #00D4FF);
    opacity: 0.6;
    animation: wave 1.4s ease-in-out infinite;
}

.waveform span:nth-child(1)  { height: 8px;  animation-delay: 0.0s; }
.waveform span:nth-child(2)  { height: 14px; animation-delay: 0.1s; }
.waveform span:nth-child(3)  { height: 22px; animation-delay: 0.2s; }
.waveform span:nth-child(4)  { height: 28px; animation-delay: 0.3s; }
.waveform span:nth-child(5)  { height: 18px; animation-delay: 0.2s; }
.waveform span:nth-child(6)  { height: 32px; animation-delay: 0.4s; }
.waveform span:nth-child(7)  { height: 22px; animation-delay: 0.3s; }
.waveform span:nth-child(8)  { height: 28px; animation-delay: 0.5s; }
.waveform span:nth-child(9)  { height: 14px; animation-delay: 0.2s; }
.waveform span:nth-child(10) { height: 20px; animation-delay: 0.1s; }
.waveform span:nth-child(11) { height: 10px; animation-delay: 0.3s; }
.waveform span:nth-child(12) { height: 6px;  animation-delay: 0.0s; }

@keyframes wave {
    0%, 100% { transform: scaleY(1); opacity: 0.5; }
    50%       { transform: scaleY(0.4); opacity: 0.9; }
}

/* ── Section header ── */
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.07);
}

/* ── Upload zone ── */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(124,58,237,0.4) !important;
    border-radius: 16px !important;
    transition: border-color 0.2s, background 0.2s;
    padding: 4px !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: rgba(124,58,237,0.7) !important;
    background: rgba(124,58,237,0.04) !important;
}

div[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    padding: 2rem !important;
}

div[data-testid="stFileUploaderDropzoneInstructions"] p,
div[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #64748B !important;
    font-size: 14px !important;
}

/* ── Selectboxes ── */
div[data-testid="stSelectbox"] > label {
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
    margin-bottom: 6px !important;
}

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #F1F5F9 !important;
    font-size: 15px !important;
    transition: border-color 0.2s !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: rgba(124,58,237,0.5) !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

/* ── Text input ── */
div[data-testid="stTextInput"] > label {
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
}

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #F1F5F9 !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}

/* ── Generate button (primary) ── */
div[data-testid="stButton"] > button[kind="primary"] {
    width: 100% !important;
    height: 56px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border-radius: 14px !important;
    border: none !important;
    background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 50%, #1D4ED8 100%) !important;
    color: white !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.35) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.5) !important;
}

div[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

/* ── Surprise Me / Theme toggle (secondary, pill-style) ── */
div[data-testid="stButton"] > button[kind="secondary"] {
    width: auto !important;
    height: 40px !important;
    padding: 0 20px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    border-radius: 999px !important;
    background: rgba(124,58,237,0.08) !important;
    border: 1px solid rgba(124,58,237,0.35) !important;
    color: #C4B5FD !important;
    box-shadow: none !important;
    display: inline-flex !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background: rgba(124,58,237,0.16) !important;
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.08) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stButton"] > button[kind="secondary"]:active {
    transform: translateY(0) scale(0.97) !important;
}

/* ── Icon helper (inline SVG inside buttons) ── */
.btn-icon {
    display: inline-flex;
    vertical-align: -3px;
    margin-right: 6px;
}

/* ── Result card ── */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px 28px 24px;
    margin-top: 2rem;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7C3AED, #00D4FF, #7C3AED);
}

.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 1rem 0 1.4rem;
}

.tag {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 13px;
    font-weight: 500;
    color: #C4B5FD;
}

.tag.cyan {
    background: rgba(0,212,255,0.1);
    border-color: rgba(0,212,255,0.3);
    color: #67E8F9;
}

/* ── Success / Info / Warning overrides ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-size: 14px !important;
}

/* ── Audio player ── */
audio {
    width: 100%;
    border-radius: 10px;
    margin-top: 8px;
    color-scheme: dark;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: rgba(0,212,255,0.1) !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    color: #67E8F9 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    height: 46px !important;
    font-size: 14px !important;
    width: 100% !important;
    box-shadow: none !important;
    transition: background 0.2s, transform 0.15s !important;
}

div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,212,255,0.18) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,212,255,0.2) !important;
}

/* ── Stat pills ── */
.stat-grid {
    display: flex;
    gap: 10px;
    margin-top: 0.4rem;
    flex-wrap: wrap;
}

.stat-pill {
    flex: 1;
    min-width: 100px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 12px 14px;
    text-align: center;
}

.stat-pill .val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #A78BFA;
}

.stat-pill .lbl {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 2px;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #475569;
    font-size: 13px;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
    letter-spacing: 0.04em;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">🎚️ &nbsp;Studio AI</div>
    <div class="hero-title">Transform <span class="accent-purple">Any Track</span><br>Into Something <span class="accent-cyan">New</span></div>
    <p class="hero-sub">Upload your audio, set the mood and genre,<br>and let the model reimagine it.</p>
    <div class="waveform">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Upload ──────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">01 &nbsp; Source File</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["mp3", "wav"],
    help="Supports MP3 and WAV files",
    label_visibility="collapsed"
)

st.write("")


# ─── Controls ────────────────────────────────────────────────────────────────

st.markdown('<p class="section-label">02 &nbsp; Sound Profile</p>', unsafe_allow_html=True)

# ── Surprise Me Presets ─────────────────────────────────────────────────────
PRESETS = [
    {"mood": "Happy",     "genre": "Pop",       "prompt": "Sunny beach vibes with upbeat energy and groovy bass"},
    {"mood": "Sad",       "genre": "Lo-fi",     "prompt": "Slow melancholic tune with soft piano and gentle rain"},
    {"mood": "Chill",     "genre": "Lo-fi",     "prompt": "Cozy coffee shop afternoon with mellow beats and vinyl crackle"},
    {"mood": "Energetic", "genre": "EDM",       "prompt": "High energy gym session with powerful drops and fast beat"},
    {"mood": "Romantic",  "genre": "Jazz",      "prompt": "Candlelight dinner with smooth jazz and soft piano"},
    {"mood": "Party",     "genre": "EDM",       "prompt": "Danceable party anthem with strong beat and fun energy"},
    {"mood": "Sad",       "genre": "Classical", "prompt": "Heartbroken late night with echo and soft strings"},
    {"mood": "Chill",     "genre": "Jazz",      "prompt": "Relaxed late night drive with soft synth and slow tempo"},
]

mood_options  = ["Happy", "Sad", "Chill", "Energetic", "Romantic", "Party"]
genre_options = ["Lo-fi", "Pop", "EDM", "Rock", "Jazz", "Classical"]

if "preset" not in st.session_state:
    st.session_state.preset = {"mood": "Chill", "genre": "Lo-fi", "prompt": ""}

surprise_col, _ = st.columns([1, 3])
with surprise_col:
    if st.button("⟲  Surprise me"):
        st.session_state.preset = random.choice(PRESETS)


col1, col2, col3 = st.columns(3)

with col1:
    mood = st.selectbox(
        "Mood",
        mood_options,
        index=mood_options.index(st.session_state.preset["mood"])
    )

with col2:
    genre = st.selectbox(
        "Genre",
        genre_options,
        index=genre_options.index(st.session_state.preset["genre"])
    )

with col3:
    quality = st.selectbox(
        "Output Quality",
        ["Standard", "High", "Ultra"],
        index=1
    )

st.write("")
st.markdown('<p class="section-label">03 &nbsp; Direction</p>', unsafe_allow_html=True)

prompt = st.text_input(
    "Describe the vibe",
    value=st.session_state.preset["prompt"],
    placeholder="e.g. Late-night study session with soft rain and warm keys…"
)

st.write("")


# ─── Generate ────────────────────────────────────────────────────────────────

generate = st.button("◆  Generate remix", type="primary")


# ─── Output ──────────────────────────────────────────────────────────────────

if generate:
    if uploaded_file is None:
        st.warning("Upload an audio file before generating.")
    else:
        audio_bytes = uploaded_file.getvalue()
        file_kb     = round(len(audio_bytes) / 1024, 1)

        # ── Step 1: Mood Detection ──────────────────────────────────────────
        with st.status("🎵 AI is working...", expanded=True) as status:

            st.write("📂 Analyzing your audio...")
            mood_result = detect_mood(audio_bytes, uploaded_file.name)

            user_selected_mood = mood  # Save user's choice

            if mood_result["success"]:
                detected_mood = mood_result["mood"]
                confidence    = mood_result["confidence"]
                # Show AI suggestion but KEEP user's selected mood
                st.write(f"🎭 AI suggests: **{detected_mood}** ({confidence}% confidence) — using your choice: **{user_selected_mood}**")
                if mood_result.get("note"):
                    st.caption(f"⚠️ {mood_result['note']}")
            else:
                confidence = 0
                st.write(f"🎭 Using selected mood: **{mood}**")

            time.sleep(0.5)

            # ── Step 2: Audio Processing ───────────────────────────────────
            st.write("🎼 Applying audio effects...")
            audio_result = apply_mood_effects(audio_bytes, uploaded_file.name, mood, genre, prompt, quality)
            if audio_result["success"]:
                st.write(f"✅ Effects applied: {', '.join(audio_result['effects_applied'][:3])}")
            time.sleep(0.5)

            # ── Step 3: Music Generation ───────────────────────────────────
            st.write("✨ Generating remix plan with Groq AI...")
            music_result = generate_music(mood, genre, prompt)

            if music_result["success"]:
                status.update(label="✅ Remix Ready!", state="complete")
            else:
                status.update(label="⚠️ Generation issue", state="error")
                st.error(music_result["error"])

        # ── Show result ─────────────────────────────────────────────────────
        if music_result["success"]:
            st.success("✅ Your remix is ready!")

            confidence_display = "Your Choice"

            # Final safety net: strip any stray backticks/angle-brackets/HTML-entities from AI text
            import html as html_module
            import re as re_module

            def _safe(text):
                t = str(text)
                t = html_module.unescape(t)              # decode &lt; &gt; &quot; etc.
                t = re_module.sub(r'<[^>]*>?', '', t)     # strip any tag-like or partial-tag content
                t = t.replace('`', '').replace('<', '').replace('>', '')
                t = re_module.sub(r'\s+', ' ', t).strip()
                return t

            safe_title       = _safe(music_result['title'])
            safe_description = _safe(music_result['description'])
            if len(safe_description) < 10:
                safe_description = f"A {mood.lower()} {genre.lower()} remix crafted to match your selected vibe."
            safe_energy      = _safe(music_result['energy_level'])
            safe_key         = _safe(music_result['key'])

            safe_filename    = _safe(uploaded_file.name)

            prompt_html = f'<p class="prompt-line">💬 "{_safe(prompt)}"</p>' if prompt.strip() else ""

            result_card_html = f"""
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                * {{ box-sizing: border-box; margin: 0; }}
                body {{ font-family: 'Inter', sans-serif; background: transparent; }}
                .result-card {{
                    background: #0F1424;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 20px;
                    padding: 28px 28px 24px;
                    position: relative;
                    overflow: hidden;
                    color: #F1F5F9;
                }}
                .result-card::before {{
                    content: '';
                    position: absolute;
                    top: 0; left: 0; right: 0;
                    height: 2px;
                    background: linear-gradient(90deg, #7C3AED, #00D4FF, #7C3AED);
                }}
                .result-title {{
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 18px; font-weight: 700;
                    color: #F1F5F9; margin-bottom: 4px;
                }}
                .result-filename {{ font-size: 13px; color: #475569; margin-bottom: 8px; }}
                .prompt-line {{ font-size: 13px; color: #A78BFA; margin-bottom: 8px; }}
                .result-desc {{ font-size: 14px; color: #94A3B8; margin-bottom: 12px; }}
                .tag-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 1rem 0 1.4rem; }}
                .tag {{
                    background: rgba(124,58,237,0.15);
                    border: 1px solid rgba(124,58,237,0.3);
                    border-radius: 8px; padding: 5px 12px;
                    font-size: 13px; font-weight: 500; color: #C4B5FD;
                }}
                .tag.cyan {{
                    background: rgba(0,212,255,0.1);
                    border-color: rgba(0,212,255,0.3);
                    color: #67E8F9;
                }}
                .stat-grid {{ display: flex; gap: 10px; flex-wrap: wrap; }}
                .stat-pill {{
                    flex: 1; min-width: 100px;
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 12px; padding: 12px 14px; text-align: center;
                }}
                .stat-pill .val {{
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 18px; font-weight: 700; color: #A78BFA;
                }}
                .stat-pill .lbl {{
                    font-size: 11px; color: #475569;
                    text-transform: uppercase; letter-spacing: 0.07em; margin-top: 2px;
                }}
            </style>
            <div class="result-card">
                <p class="result-title">{safe_title}</p>
                <p class="result-filename">{safe_filename}</p>
                {prompt_html}
                <p class="result-desc">{safe_description}</p>
                <div class="tag-row">
                    <span class="tag">🎭 {mood}</span>
                    <span class="tag">🎵 {genre}</span>
                    <span class="tag cyan">🎧 {quality}</span>
                    <span class="tag">⚡ {safe_energy}</span>
                </div>
                <div class="stat-grid">
                    <div class="stat-pill"><div class="val">{music_result['bpm']}</div><div class="lbl">BPM</div></div>
                    <div class="stat-pill"><div class="val">{confidence_display}</div><div class="lbl">Mood Source</div></div>
                    <div class="stat-pill"><div class="val">{safe_key}</div><div class="lbl">Key</div></div>
                </div>
            </div>
            """

            # Absolute final guard: backticks anywhere break rendering
            result_card_html = result_card_html.replace('`', "'")

            components.html(result_card_html, height=320, scrolling=True)

            st.write("")

            # Applied audio effects
            if audio_result["success"] and audio_result.get("effects_applied"):
                st.markdown("**🎛️ Audio Effects Applied:**")
                for effect in audio_result["effects_applied"]:
                    st.caption(f"• {effect}")
                st.write("")

            # Instruments
            if music_result.get("instruments"):
                st.markdown("**🎸 Suggested Instruments:**")
                cols = st.columns(len(music_result["instruments"]))
                for i, inst in enumerate(music_result["instruments"]):
                    with cols[i]:
                        st.info(inst)

            # Remix Tips
            if music_result.get("remix_tips"):
                st.markdown("**💡 AI Remix Tips:**")
                for tip in music_result["remix_tips"]:
                    st.success(f"→ {tip}")

            st.write("")

            # ── Before / After Comparison ────────────────────────────────────
            import base64

            original_b64 = base64.b64encode(uploaded_file.getvalue()).decode()
            original_mime = "audio/wav" if uploaded_file.name.lower().endswith(".wav") else "audio/mpeg"

            if audio_result["success"]:
                remix_b64 = base64.b64encode(audio_result["audio_bytes"]).decode()
            else:
                remix_b64 = original_b64
            remix_mime = "audio/mpeg"

            st.markdown("**🎧 Before / After Comparison:**")

            comparison_html = f"""
            <div style="display:flex; gap:16px; font-family:'Inter',sans-serif;">
                <div style="flex:1;">
                    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                              color:#475569;margin-bottom:8px;">Original</p>
                    <audio id="originalAudio" controls style="width:100%;">
                        <source src="data:{original_mime};base64,{original_b64}" type="{original_mime}">
                    </audio>
                </div>
                <div style="flex:1;">
                    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;
                              color:#475569;margin-bottom:8px;">Remixed</p>
                    <audio id="remixAudio" controls style="width:100%;">
                        <source src="data:{remix_mime};base64,{remix_b64}" type="{remix_mime}">
                    </audio>
                </div>
            </div>
            <script>
                const orig  = document.getElementById('originalAudio');
                const remix = document.getElementById('remixAudio');
                orig.addEventListener('play', function() {{ remix.pause(); }});
                remix.addEventListener('play', function() {{ orig.pause(); }});
            </script>
            """

            components.html(comparison_html, height=100)

            st.write("")

            # Download button
            if audio_result["success"]:
                st.download_button(
                    "↓  Download Remix",
                    audio_result["audio_bytes"],
                    file_name=f"remix_{uploaded_file.name}",
                    mime="audio/mp3"
                )
            else:
                st.download_button(
                    "↓  Download Remix",
                    uploaded_file,
                    file_name=f"remix_{uploaded_file.name}",
                    mime="audio/wav"
                )

        else:
            st.error(f"❌ {music_result['error']}")
            st.info("Showing original track.")
            st.audio(uploaded_file)


# ─── Footer ──────────────────────────────────────────────────────────────────

st.markdown(
    "<div class='footer'>Studio AI &nbsp;·&nbsp; Powered by Streamlit</div>",
    unsafe_allow_html=True
)
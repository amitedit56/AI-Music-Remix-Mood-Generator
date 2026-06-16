<div align="center">

# 🎵 AI Music Remix & Mood Generator

**Transform any track into something new — powered by AI**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA%203-00D4FF?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.12-7C3AED?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

[🚀 Live Demo](https://your-app-url.streamlit.app) &nbsp;|&nbsp; [📂 GitHub](https://github.com/amitedit56/AI-Music-Remix-Mood-Generator)

---

</div>

## 🎯 Problem Statement

Remixing or creating music usually requires technical skills and expensive software — which most students don't have. **AI Music Remix & Mood Generator** solves this by letting anyone upload a song, pick a mood and genre, and instantly get an AI-generated remix plan with real audio effects applied.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎭 **AI Mood Detection** | Analyzes uploaded audio using `librosa` — detects tempo, energy & brightness |
| 🤖 **Groq AI Remix Plan** | Generates title, BPM, key, instruments & remix tips using LLaMA 3.3 70B |
| 🎼 **Real Audio Effects** | Applies speed, volume, lo-fi filter & fade effects via `pydub` |
| 💬 **Vibe Description** | Keyword-aware prompt engine — "slow", "bass", "echo" trigger specific effects |
| 🎲 **Surprise Me** | One-click random mood + genre + prompt preset |
| 🔊 **Before / After Player** | Side-by-side original vs remixed audio comparison |
| ⬇️ **Download Remix** | Export processed audio as MP3 |

---

## 🛠️ Tech Stack

```
Frontend      →  Streamlit
AI / LLM      →  Groq API  (llama-3.3-70b-versatile)
Audio Analysis→  librosa + numpy
Audio Effects →  pydub + ffmpeg
Deployment    →  Streamlit Community Cloud
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- ffmpeg installed (`winget install ffmpeg` on Windows)
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/amitedit56/AI-Music-Remix-Mood-Generator.git
cd AI-Music-Remix-Mood-Generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo GROQ_API_KEY=your_groq_key_here > .env

# 4. Run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
AI-Music-Remix-Mood-Generator/
│
├── app.py                  # Main Streamlit frontend
├── backend/
│   ├── mood_detector.py    # librosa audio analysis
│   ├── music_generator.py  # Groq AI remix plan generator
│   └── audio_utils.py      # pydub audio effects engine
├── .streamlit/
│   └── config.toml         # Dark theme config
├── requirements.txt
└── packages.txt            # System packages (ffmpeg)
```

---

## 🎬 How It Works

```
Upload MP3/WAV
      ↓
librosa analyzes tempo, energy & brightness → detects mood
      ↓
pydub applies real audio effects (speed, volume, lo-fi)
      ↓
Groq LLaMA 3.3 generates remix plan (title, BPM, key, tips)
      ↓
Before/After comparison player + Download
```

---

## 📸 Screenshots

> Upload your song → select mood & genre → get AI remix plan with real audio processing
<img width="872" height="820" alt="image" src="https://github.com/user-attachments/assets/c9450e1f-a13d-40fe-a1dc-c69410eaa0fa" />
<img width="872" height="820" alt="image" src="https://github.com/user-attachments/assets/1fcca146-c33e-44ea-a5d4-78d70094dd70" />
<img width="872" height="820" alt="image" src="https://github.com/user-attachments/assets/9a3c8e6c-5471-4c18-b3d4-e71e87ebfb42" />
<img width="872" height="820" alt="image" src="https://github.com/user-attachments/assets/3b3a7199-d4e2-4467-af75-d3001cfa22ee" />

---

<div align="center">

Made with ❤️ for internship demo &nbsp;|&nbsp; **Studio AI**

</div>

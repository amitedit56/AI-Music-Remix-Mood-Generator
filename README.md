<div align="center">

# 🎵 AI Music Remix & Mood Generator

**Transform any track into something new — powered by AI**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA%203-00D4FF?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.12-7C3AED?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

[🚀 Live Demo](https://ai-music-remix-mood-generator-app9iuqjjd2ry9ur2dyh6wx.streamlit.app/) &nbsp;|&nbsp; [📂 GitHub](https://github.com/amitedit56/AI-Music-Remix-Mood-Generator)

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

> Upload your song → select mood & genre → get AI remix plan with real audio processing>
<img width="1177" height="841" alt="Screenshot 2026-06-16 092717" src="https://github.com/user-attachments/assets/f8b85ee6-4e0e-45a5-9b59-0b786f4d40f0" />
<img width="1165" height="842" alt="image" src="https://github.com/user-attachments/assets/288617d3-01e2-4f6d-8224-7b28dd3d0965" />
<img width="1192" height="702" alt="image" src="https://github.com/user-attachments/assets/6fcd2064-39f5-46b5-8899-463496b0368c" />
<img width="1235" height="841" alt="image" src="https://github.com/user-attachments/assets/c4baa1d3-7fa7-43ea-8871-46e268740829" />

---

<div align="center">

Made with ❤️ for internship Project &nbsp;|&nbsp; **Studio AI**

</div>

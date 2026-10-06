# TrailEcho - Offline Wilderness Safety & Screen-Free Audio Companion

TrailEcho is an open-source, screen-free wilderness companion engineered for hikers, foragers, and trail runners. Built with **Google Gemma 2**, **ElevenLabs Voice Synthesis**, and **TabPFN micro-climate risk heuristics**, TrailEcho keeps your eyes off the screen and your ears tuned to nature.

## 🌲 Why TrailEcho? (Touch Grass Philosophy)
The goal of outdoors adventure is to experience reality, not stare at a smartphone. But in deep wilderness with **zero cellular signal**, unexpected mountain storms, poisonous lookalikes, and rapid temperature drops can become life-threatening.

TrailEcho solves this dilemma:
1. **Screen-Free Audio First**: Tap a single button on your pocket or bone-conduction headphones. Audio delivers critical safety alerts in seconds.
2. **Offline-Resilient Architecture**: Built-in offline heuristics and fallbacks ensure survival triage works even with zero bars of signal.
3. **Dual Intelligence Engine**:
   - **Google Gemma 2**: Structured wilderness triage, toxic lookalike differentiation, and emergency response instructions.
   - **TabPFN/Micro-Climate Risk Predictor**: Calculates hypothermia and storm onset probability from elevation, barometric pressure trend, and humidity.
   - **ElevenLabs High-Fidelity Audio**: Generates clear, calming natural voice alerts with automatic Web Speech fallback.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- Google AI Studio API key (`GEMINI_API_KEY`)
- Optional: ElevenLabs API key (`ELEVENLABS_API_KEY`)

### Local Installation
```bash
git clone https://github.com/Hao610/trailecho-gemma.git
cd trailecho-gemma
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run app.py
```

### Running Tests
```bash
pytest tests/ -v
```

---

## 🌐 Deploy to Render

1. Fork or push this repository to GitHub: `https://github.com/Hao610/trailecho-gemma`
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** -> **Web Service**.
4. Connect `trailecho-gemma` repository.
5. In Settings:
   - **Name**: `trailecho-gemma`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
6. Under **Environment Variables**, add:
   - `GEMINI_API_KEY`: Your Google AI Studio API key
   - `ELEVENLABS_API_KEY`: (Optional) Your ElevenLabs API key

---

## ⚖️ License
Apache-2.0 License. Open source for Hacktoberfest 2026.

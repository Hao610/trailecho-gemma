"""
TrailEcho - Screen-Free Offline Wilderness & Trail Companion
Built for Hacktoberfest 2026: Open-Source AI Challenge (Touch Grass)
"""

import os
import streamlit as st
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from src.gemma_engine import analyze_wilderness_query
from src.tabpfn_climate import predict_trail_risk
from src.audio_engine import synthesize_voice_alert
from src.knowledge_base import OFFLINE_SURVIVAL_DATABASE

load_dotenv()

st.set_page_config(
    page_title="TrailEcho | Screen-Free Wilderness Companion",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Outdoor HUD Styling
st.markdown("""
<style>
    .trail-hud-header {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
        color: #d8f3dc;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #52b788;
    }
    .hud-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hud-subtitle {
        font-size: 1.05rem;
        color: #b7e4c7;
        margin-top: 0.3rem;
    }
    .audio-card {
        background: #081c15;
        border: 2px solid #52b788;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge-critical {
        background-color: #d90429;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-caution {
        background-color: #f77f00;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
    .badge-safe {
        background-color: #2d6a4f;
        color: #d8f3dc;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
<div class="trail-hud-header">
    <div class="hud-title">🌲 TrailEcho: Wilderness Audio Companion</div>
    <div class="hud-subtitle">Screen-free outdoor safety powered by <b>Google Gemma 2</b>, <b>ElevenLabs</b> & <b>TabPFN Heuristics</b></div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Trail Hardware & API Configuration
with st.sidebar:
    st.header("⚙️ Trail Rig & Keys")
    gemini_key = st.text_input(
        "Google Gemini / Gemma Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Google AI Studio key for Gemma 2 reasoning. Leave empty for offline mode."
    )
    elevenlabs_key = st.text_input(
        "ElevenLabs API Key",
        value=os.getenv("ELEVENLABS_API_KEY", ""),
        type="password",
        help="Optional: Generates ultra-realistic voice cues. Falls back to browser audio."
    )
    
    st.markdown("---")
    st.subheader("📡 Simulated Trail Barometer")
    elevation = st.slider("Elevation (Meters)", 0, 4500, 1450, step=50)
    temp = st.slider("Ambient Temp (°C)", -15.0, 35.0, 8.0, step=0.5)
    humidity = st.slider("Relative Humidity (%)", 10, 100, 85)
    pressure = st.number_input("Barometric Pressure (hPa)", value=1012.0, step=0.5)
    pressure_delta = st.slider("3-Hour Pressure Shift (hPa)", -8.0, 4.0, -3.5, step=0.5,
                               help="A rapid drop (> 2 hPa in 3h) signals an incoming mountain tempest.")
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 80.0, 28.0, step=1.0)
    
    st.markdown("---")
    st.caption("🏆 Built for **Hacktoberfest 2026** DEV Challenge: Week 1 'Touch Grass'.")

# Main Interface: Two Column Field Layout
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
    st.subheader("🎧 Hands-Free Voice Query")
    st.caption("Keep your phone in your backpack. Tap one prompt below or enter an emergency situation:")

    # Quick Trail Scenario Buttons
    scenarios = [
        "White capped mushroom with a ring and cup at base. Can I forage it?",
        "Shivering uncontrollably and fingers are losing sensation in sudden sleet.",
        "Rattled noise in the tall grass and a painful double puncture on ankle.",
        "Dark purple berries growing along the creek bank, are they edible?"
    ]
    
    chosen_scenario = None
    cols_btn = st.columns(2)
    for i, s in enumerate(scenarios):
        if cols_btn[i % 2].button(f"Scenario {i+1}", help=s, use_container_width=True):
            chosen_scenario = s

    trail_query = st.text_area(
        "Voice Input / Observation:",
        value=chosen_scenario if chosen_scenario else "Found a cluster of smooth white mushrooms under an oak tree. One has white gills and an egg-like cup at the base.",
        height=90
    )

    execute_btn = st.button("📡 Broadcast to Earphones (Ask TrailEcho)", type="primary", use_container_width=True)

    if execute_btn and trail_query.strip():
        with st.spinner("Analyzing via Gemma 2 wilderness heuristics..."):
            result = analyze_wilderness_query(
                query=trail_query,
                elevation_meters=elevation,
                temp_celsius=temp,
                api_key=gemini_key
            )

        hazard = result.get("hazard_level", "MODERATE")
        badge_class = "badge-critical" if hazard in ["CRITICAL", "LETHAL", "HIGH"] else "badge-caution" if hazard in ["MODERATE", "HIGH_IRRITANT"] else "badge-safe"

        st.markdown(f"""
        <div class="audio-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #74c69d;">{result.get('topic', 'Wilderness Safety')}</h3>
                <span class="{badge_class}">{hazard}</span>
            </div>
            <p style="font-size: 1.15rem; color: #ffffff; margin-top: 0.8rem; font-style: italic;">
                🔊 "{result.get('voice_cue', '')}"
            </p>
            <div style="font-size: 0.85rem; color: #95d5b2;">
                Engine: {result.get('engine', 'Gemma 2 Offline Matrix')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Audio Generation (ElevenLabs or HTML5 TTS)
        voice_cue = result.get("voice_cue", "")
        if voice_cue:
            audio_bytes, audio_msg = synthesize_voice_alert(voice_cue, api_key=elevenlabs_key)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                st.caption(f"✨ {audio_msg}")
            else:
                st.info(f"🔊 Headphone Audio Prompt: '{voice_cue}'")
                # Fallback to browser HTML5 SpeechSynthesis
                st.components.v1.html(f"""
                <script>
                    if ('speechSynthesis' in window) {{
                        const utterance = new SpeechSynthesisUtterance({repr(voice_cue)});
                        utterance.rate = 1.0;
                        utterance.pitch = 1.0;
                        window.speechSynthesis.speak(utterance);
                    }}
                </script>
                """, height=0)

        # Immediate Actions
        st.write("##### 🛠️ Immediate Field Action Steps")
        for step in result.get("immediate_actions", []):
            st.markdown(f"- **{step}**")

        # Toxic Lookalikes
        lookalikes = result.get("toxic_lookalikes", [])
        if lookalikes and lookalikes != ["None"]:
            st.warning("⚠️ **Fatal Lookalike Alert:**")
            for item in lookalikes:
                st.markdown(f"- 🍄 {item}")

with col_right:
    st.subheader("📊 TabPFN Micro-Climate & Hypothermia HUD")
    st.caption("Predicts mountain storm front and hypothermia onset using environmental telemetry.")

    climate_risk = predict_trail_risk(
        elevation_meters=elevation,
        temp_celsius=temp,
        humidity_percent=humidity,
        pressure_hpa=pressure,
        pressure_delta_3h=pressure_delta,
        wind_speed_kmh=wind_speed
    )

    risk_status = climate_risk["status"]
    status_color = "#d90429" if risk_status == "CRITICAL" else "#f77f00" if risk_status == "ELEVATED" else "#2d6a4f"

    st.markdown(f"""
    <div style="background: #111e17; border-left: 5px solid {status_color}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <h4 style="margin: 0; color: {status_color};">Climate Status: {risk_status}</h4>
        <p style="margin: 0.4rem 0 0 0; color: #d8f3dc; font-size: 0.95rem;">{climate_risk['voice_alert']}</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Effective Wind Chill", f"{climate_risk['effective_temp_c']} °C")
    m2.metric("Storm Risk", f"{climate_risk['storm_probability_pct']}%")
    m3.metric("Hypothermia Risk", f"{climate_risk['hypothermia_risk_pct']}%")

    st.write("##### 🧭 Trail Environmental Readout")
    for rec in climate_risk["recommendations"]:
        st.markdown(f"- {rec}")

    st.markdown("---")
    st.subheader("🎒 Offline Knowledge Base (No Signal)")
    st.caption("Emergency survival cards stored locally in flash memory:")
    for key, data in OFFLINE_SURVIVAL_DATABASE.items():
        with st.expander(f"{data['title']} ({data['severity']})"):
            st.markdown(f"**Earphone Cue**: *\"{data['voice_alert']}\"*")
            for step in data["action_steps"]:
                st.markdown(f"- {step}")
            if data["toxic_lookalikes"]:
                st.error(f"Lookalike Warning: {', '.join(data['toxic_lookalikes'])}")

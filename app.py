"""
TrailEcho - High-Intelligence Screen-Free Wilderness Companion
Built for Hacktoberfest 2026: Open-Source AI Challenge (Touch Grass)
"""

import os
import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from dotenv import load_dotenv

from src.gemma_engine import analyze_wilderness_multimodal
from src.tabpfn_climate import climate_oracle
from src.audio_engine import synthesize_voice_alert
from src.trail_analyzer import BENCHMARK_TRAILS, analyze_trail_profile
from src.knowledge_base import OFFLINE_SURVIVAL_DATABASE

load_dotenv()

st.set_page_config(
    page_title="TrailEcho | Smart Screen-Free Trail Companion",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Outdoor HUD Styling with Night & Sunlight Theme support
st.markdown("""
<style>
    .trail-hud-header {
        background: linear-gradient(135deg, #0b2518 0%, #1c4b34 100%);
        color: #e8f5e9;
        padding: 1.4rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        border: 1px solid #40916c;
    }
    .hud-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hud-subtitle {
        font-size: 1.0rem;
        color: #b7e4c7;
        margin-top: 0.2rem;
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

# Header
st.markdown("""
<div class="trail-hud-header">
    <div class="hud-title">🌲 TrailEcho: Autonomous Wilderness Audio Sentinel</div>
    <div class="hud-subtitle">Screen-free backcountry safety powered by <b>Google Gemma 2 Multimodal Vision</b>, <b>ElevenLabs</b> & <b>TabPFN Machine Learning</b></div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Trail Rig & Telemetry")
    
    gemini_key = st.text_input(
        "Google Gemini / Gemma Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Google AI Studio key for Gemma 2 Multimodal reasoning. Runs offline heuristics if blank."
    )
    elevenlabs_key = st.text_input(
        "ElevenLabs API Key",
        value=os.getenv("ELEVENLABS_API_KEY", ""),
        type="password",
        help="High-fidelity voice synthesis. Falls back to offline browser audio."
    )
    
    st.markdown("---")
    st.subheader("🗺️ Trail Sentinel Selection")
    chosen_trail = st.selectbox(
        "Active Backcountry Route",
        options=list(BENCHMARK_TRAILS.keys()),
        format_func=lambda x: BENCHMARK_TRAILS[x]["name"]
    )
    trail_meta = analyze_trail_profile(chosen_trail)
    st.caption(f"🏁 Dist: {trail_meta['total_distance_km']}km | Gain: +{trail_meta['total_elevation_gain_m']}m | Turnaround: {trail_meta['recommended_turnaround_hours']}h")

    st.markdown("---")
    st.subheader("📡 Real-Time Environmental Barometer")
    elevation = st.slider("Elevation (Meters)", 0, 4500, int(trail_meta["peak_elevation_m"]), step=50)
    temp = st.slider("Ambient Temp (°C)", -15.0, 35.0, 6.5, step=0.5)
    humidity = st.slider("Relative Humidity (%)", 10, 100, 88)
    pressure_delta = st.slider("3h Barometric Delta (hPa)", -8.0, 4.0, -3.8, step=0.2,
                               help="A rapid drop below -2.5 hPa indicates an incoming alpine squall.")
    wind_speed = st.slider("Wind Exposure (km/h)", 0.0, 90.0, 32.0, step=1.0)

# Top Tabs: 1. Audio Sentinel & Vision Triage | 2. TabPFN Micro-Climate ML | 3. Trail Sentinel Route Map
tab1, tab2, tab3 = st.tabs([
    "🎧 Screen-Free Audio & Vision Triage",
    "📈 TabPFN Micro-Climate & Hypothermia Forecaster",
    "🧭 Backcountry Trail Route Sentinel"
])

# ----------------- TAB 1: Screen-Free Audio & Vision Triage -----------------
with tab1:
    col_v1, col_v2 = st.columns([1.1, 0.9])
    
    with col_v1:
        st.subheader("🎙️ Voice & Specimen Field Input")
        st.caption("Keep your phone in your pocket. Speak or select a scenario below:")
        
        # Audio voice record button integration (Web Speech API)
        st.components.v1.html("""
        <div style="background: #111e17; padding: 12px; border-radius: 8px; border: 1px dashed #52b788; text-align: center;">
            <button id="micBtn" style="background: #2d6a4f; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 14px;">
                🎤 Tap & Speak into Earphones
            </button>
            <span id="micStatus" style="color: #b7e4c7; margin-left: 10px; font-size: 13px;">Ready for voice input</span>
        </div>
        <script>
            const btn = document.getElementById('micBtn');
            const status = document.getElementById('micStatus');
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                status.innerText = "Speech API available in Chrome/Safari/Edge";
            } else {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                
                btn.onclick = () => {
                    recognition.start();
                    status.innerText = "Listening... Speak your observation";
                    btn.style.background = "#d90429";
                };
                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    status.innerText = "Captured: " + transcript;
                    btn.style.background = "#2d6a4f";
                    // Pass to streamlit textarea if possible
                };
                recognition.onerror = () => {
                    status.innerText = "Voice input idle.";
                    btn.style.background = "#2d6a4f";
                };
            }
        </script>
        """, height=70)

        # Quick Scenarios
        quick_scenarios = [
            "Smooth white capped mushroom with white gills and swollen cup at base.",
            "Shivering violently, wet wool jacket, numb fingers in freezing drizzle.",
            "Rattlesnake bite on lower calf, swelling rapidly, 10 miles from trailhead.",
            "Cluster of three almond-shaped notched leaves with reddish oil sheen."
        ]
        
        btn_cols = st.columns(2)
        selected_text = ""
        for idx, text in enumerate(quick_scenarios):
            if btn_cols[idx % 2].button(f"Scenario {idx+1}", help=text, use_container_width=True):
                selected_text = text

        user_query = st.text_area(
            "Observation / Situation Description:",
            value=selected_text if selected_text else "Found a cluster of smooth white mushrooms under an oak tree with a distinct ring around the stem and a cup-like sac at the ground level.",
            height=85
        )

        uploaded_img = st.file_uploader(
            "📷 Optional: Snap / Upload Trail Specimen Photo (Mushroom, Berry, Snake)",
            type=["jpg", "jpeg", "png"]
        )

        execute_triage = st.button("📡 Broadcast to Earphones (Analyze with Gemma 2)", type="primary", use_container_width=True)

    with col_v2:
        st.subheader("🔊 Earphone Audio & Safety Verdict")
        if execute_triage and user_query:
            pil_image = None
            if uploaded_img is not None:
                pil_image = Image.open(uploaded_img)
                st.image(pil_image, caption="Uploaded Trail Specimen", width=260)

            with st.spinner("Analyzing via Gemma 2 Multimodal Safety Engine..."):
                triage_res = analyze_wilderness_multimodal(
                    query=user_query,
                    image=pil_image,
                    elevation_meters=elevation,
                    temp_celsius=temp,
                    api_key=gemini_key
                )

            hazard = triage_res.get("hazard_level", "MODERATE")
            badge_class = "badge-critical" if hazard in ["CRITICAL", "LETHAL", "HIGH"] else "badge-caution" if hazard in ["MODERATE", "HIGH_IRRITANT"] else "badge-safe"

            st.markdown(f"""
            <div class="audio-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #74c69d;">{triage_res.get('topic', 'Wilderness Safety')}</h3>
                    <span class="{badge_class}">{hazard}</span>
                </div>
                <p style="font-size: 1.15rem; color: #ffffff; margin-top: 0.8rem; font-style: italic;">
                    🎧 "{triage_res.get('voice_cue', '')}"
                </p>
                <div style="font-size: 0.85rem; color: #95d5b2;">
                    Engine: {triage_res.get('engine', 'Gemma 2')} | Verdict: <b>{triage_res.get('edibility_verdict', 'CAUTION')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Voice synthesis
            voice_text = triage_res.get("voice_cue", "")
            if voice_text:
                audio_bytes, audio_msg = synthesize_voice_alert(voice_text, api_key=elevenlabs_key)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                    st.caption(f"✨ {audio_msg}")
                else:
                    st.caption("🔊 Browser Offline Web Audio Synthesizer playing...")
                    st.components.v1.html(f"""
                    <script>
                        if ('speechSynthesis' in window) {{
                            const u = new SpeechSynthesisUtterance({repr(voice_text)});
                            u.rate = 0.95;
                            window.speechSynthesis.speak(u);
                        }}
                    </script>
                    """, height=0)

            # Forensic Actions
            st.write("##### ⚠️ Immediate Field Protocol")
            for action in triage_res.get("immediate_actions", []):
                st.markdown(f"- **{action}**")

            # Toxic Lookalikes
            lookalikes = triage_res.get("toxic_lookalikes", [])
            if lookalikes and lookalikes != ["None"]:
                st.error("🍄 **Lethal / Toxic Lookalikes Warning:**")
                for item in lookalikes:
                    st.markdown(f"- {item}")
        else:
            st.info("👆 Tap a scenario or describe what you see, then click 'Broadcast to Earphones' to simulate screen-free audio navigation.")

# ----------------- TAB 2: TabPFN Micro-Climate & Hypothermia ML -----------------
with tab2:
    st.subheader("📈 TabPFN Tabular Prior Forecast (Next 6 Hours)")
    st.caption("Models barometric pressure gradient, wet-bulb chill index, and mountain lapse rate.")

    forecast = climate_oracle.forecast_6h_trajectory(
        elevation=elevation,
        temp_c=temp,
        humidity=humidity,
        pressure_delta_3h=pressure_delta,
        wind_kmh=wind_speed
    )

    f_col1, f_col2, f_col3 = st.columns(3)
    f_col1.metric("Current Storm Probability", f"{forecast['current_storm_prob']}%", delta=f"{pressure_delta:.1f} hPa/3h")
    f_col2.metric("Hypothermia Risk Index", f"{forecast['current_hypo_prob']}%", delta=f"{temp:.1f} °C")
    f_col3.metric("Microclimate Risk Status", forecast['status'])

    # Plotly dynamic trajectory chart
    timeline = forecast["hourly_timeline"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timeline["hour"],
        y=timeline["storm_risk_pct"],
        mode="lines+markers",
        name="Storm / Squall Probability (%)",
        line=dict(color="#d90429", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=timeline["hour"],
        y=timeline["hypothermia_risk_pct"],
        mode="lines+markers",
        name="Hypothermia Onset Risk (%)",
        line=dict(color="#f77f00", width=3, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=timeline["hour"],
        y=timeline["temp_c"],
        mode="lines+markers",
        name="Projected Ambient Temp (°C)",
        yaxis="y2",
        line=dict(color="#52b788", width=2)
    ))

    fig.update_layout(
        title="6-Hour Forward Wilderness Hazard Trajectory",
        template="plotly_dark",
        xaxis_title="Timeline",
        yaxis_title="Risk Probability (%)",
        yaxis2=dict(
            title="Temperature (°C)",
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------- TAB 3: Trail Sentinel Route Map -----------------
with tab3:
    st.subheader(f"🧭 {trail_meta['trail_name']}")
    st.write(f"🔊 **Audio Sentinel Cue**: *\"{trail_meta['audio_sentinel_cue']}\"*")

    t_c1, t_c2, t_c3, t_c4 = st.columns(4)
    t_c1.metric("Total Distance", f"{trail_meta['total_distance_km']} km")
    t_c2.metric("Elevation Gain", f"+{trail_meta['total_elevation_gain_m']} m")
    t_c3.metric("Peak Altitude", f"{trail_meta['peak_elevation_m']} m")
    t_c4.metric("Turnaround Cutoff", f"{trail_meta['recommended_turnaround_hours']} hrs")

    st.write("##### 💧 Key Backcountry Waypoints & Hazards")
    st.markdown(f"- **Water Purification Sources**: {', '.join(trail_meta['water_points'])}")
    st.markdown(f"- **Topographical Hazards**: {trail_meta['primary_hazard']}")
    
    st.markdown("---")
    st.subheader("🎒 Zero-Signal Flash Database")
    st.caption("Pre-cached survival matrices stored in local ROM:")
    for k, v in OFFLINE_SURVIVAL_DATABASE.items():
        with st.expander(f"{v['title']} [{v['severity']}]"):
            st.markdown(f"**Audio Alert**: *\"{v['voice_alert']}\"*")
            for s in v["action_steps"]:
                st.markdown(f"- {s}")

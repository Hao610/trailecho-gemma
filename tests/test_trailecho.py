"""
Unit tests for TrailEcho Wilderness Companion.
Tests offline heuristics, climate risk calculations, and audio synthesis fallbacks.
"""

import pytest
from src.knowledge_base import lookup_offline_emergency, OFFLINE_SURVIVAL_DATABASE
from src.tabpfn_climate import calculate_wind_chill, predict_trail_risk
from src.gemma_engine import analyze_wilderness_query
from src.audio_engine import synthesize_voice_alert


def test_offline_emergency_lookup():
    """Verify offline fallback matches known wilderness hazards."""
    res = lookup_offline_emergency("death_cap")
    assert res["severity"] == "LETHAL"
    assert "amatoxins" in res["voice_alert"].lower()
    assert len(res["action_steps"]) > 0

    hypo = lookup_offline_emergency("I feel hypothermia and cold")
    assert hypo["severity"] == "CRITICAL"


def test_unknown_emergency_fallback():
    """Verify safe fallback for unknown queries."""
    res = lookup_offline_emergency("random obscure rock formation")
    assert res["severity"] == "MODERATE"
    assert "stop" in res["voice_alert"].lower()


def test_wind_chill_calculation():
    """Verify wind chill formula accuracy."""
    # When warm or low wind, temp remains unchanged
    assert calculate_wind_chill(15.0, 20.0) == 15.0
    # When freezing and windy, perceived temp drops significantly
    chilled = calculate_wind_chill(-5.0, 30.0)
    assert chilled < -5.0


def test_tabpfn_climate_prediction():
    """Verify micro-climate risk assessment."""
    risk = predict_trail_risk(
        elevation_meters=2200,
        temp_celsius=2.0,
        humidity_percent=90.0,
        pressure_hpa=995.0,
        pressure_delta_3h=-4.5,
        wind_speed_kmh=45.0
    )
    assert risk["status"] == "CRITICAL"
    assert risk["storm_probability_pct"] > 70.0
    assert risk["hypothermia_risk_pct"] > 70.0
    assert "Urgent" in risk["voice_alert"]


def test_gemma_engine_offline_execution():
    """Verify Gemma engine degrades gracefully without API keys."""
    res = analyze_wilderness_query(
        query="hypothermia",
        elevation_meters=1500,
        temp_celsius=4.0,
        api_key=""
    )
    assert res["hazard_level"] == "CRITICAL"
    assert len(res["immediate_actions"]) > 0
    assert "Offline" in res["engine"]


def test_elevenlabs_fallback():
    """Verify audio engine degrades gracefully without key."""
    audio_bytes, msg = synthesize_voice_alert("Take shelter now.", api_key=None)
    assert audio_bytes is None
    assert "Web Speech API" in msg

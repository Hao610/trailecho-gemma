"""
Updated unit test suite for TrailEcho.
Tests TabPFN ML classifier, Multimodal Gemma heuristics, and Trail Sentinel.
"""

import pytest
from src.knowledge_base import lookup_offline_emergency
from src.tabpfn_climate import climate_oracle
from src.gemma_engine import analyze_wilderness_multimodal
from src.trail_analyzer import analyze_trail_profile


def test_trail_sentinel_profile():
    profile = analyze_trail_profile("Rainier_Skyline_Loop")
    assert profile["total_distance_km"] == 9.3
    assert profile["peak_elevation_m"] == 2140
    assert profile["recommended_turnaround_hours"] == 4.5
    assert len(profile["water_points"]) > 0


def test_tabpfn_ml_forecaster():
    # Extreme weather: deep barometric plunge (-4.5 hPa), high altitude, sub-zero
    fc = climate_oracle.forecast_6h_trajectory(
        elevation=2800,
        temp_c=-2.0,
        humidity=92.0,
        pressure_delta_3h=-5.0,
        wind_kmh=65.0
    )
    assert fc["status"] == "CRITICAL_HAZARD"
    assert fc["current_storm_prob"] > 60.0
    assert len(fc["hourly_timeline"]["hour"]) == 7
    assert fc["hourly_timeline"]["storm_risk_pct"][-1] > 50.0


def test_gemma_multimodal_offline():
    res = analyze_wilderness_multimodal(
        query="white mushroom with swollen cup volva",
        image=None,
        elevation_meters=1200,
        temp_celsius=14.0,
        api_key=""
    )
    assert res["hazard_level"] in ["CRITICAL", "LETHAL"]
    assert "amatoxins" in res["voice_cue"].lower() or "death cap" in res["topic"].lower()
    assert len(res["immediate_actions"]) > 0

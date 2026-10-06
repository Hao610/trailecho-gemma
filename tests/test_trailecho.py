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


def test_field_journal():
    from src.field_journal import TrailFieldJournal
    journal = TrailFieldJournal()
    entry = journal.add_entry(
        topic="Death Cap",
        hazard_level="LETHAL",
        voice_cue="Extreme Hazard",
        elevation=1400,
        temp_c=12.0,
        notes="Found near roots"
    )
    assert entry["id"] == "log-001"
    assert len(journal.logs) == 1
    assert "log-001" in journal.export_json()


def test_metabolism_and_daylight():
    from src.metabolism_daylight import calculate_daylight_horizon, calculate_backcountry_metabolism
    daylight = calculate_daylight_horizon(current_hour=17.5, sunset_hour=18.5)
    assert daylight["status"] == "CRITICAL_DUSK"
    assert "Urgent" in daylight["voice_cue"]

    metabolism = calculate_backcountry_metabolism(
        hiker_weight_kg=70.0,
        pack_weight_kg=10.0,
        distance_km=10.0,
        elevation_gain_m=500.0,
        temp_celsius=20.0
    )
    assert metabolism["total_calories_burned_kcal"] > 800
    assert metabolism["water_required_liters"] > 1.0

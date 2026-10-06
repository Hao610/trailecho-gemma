"""
TabPFN-inspired Micro-Climate & Trail Hypothermia Risk Predictor.
Calculates wilderness hazards based on barometric pressure gradients,
wind chill index, altitude lapse rate, and humidity.
"""

from typing import Dict, Any
import numpy as np


def calculate_wind_chill(temp_celsius: float, wind_speed_kmh: float) -> float:
    """Calculate perceived wind chill using the North American formula."""
    if wind_speed_kmh < 4.8 or temp_celsius > 10.0:
        return temp_celsius
    wc = 13.12 + (0.6215 * temp_celsius) - (11.37 * (wind_speed_kmh ** 0.16)) + (0.3965 * temp_celsius * (wind_speed_kmh ** 0.16))
    return round(wc, 1)


def predict_trail_risk(
    elevation_meters: float,
    temp_celsius: float,
    humidity_percent: float,
    pressure_hpa: float,
    pressure_delta_3h: float,
    wind_speed_kmh: float
) -> Dict[str, Any]:
    """
    Predicts storm and hypothermia probability using tabular meteorological heuristics.
    Simulates TabPFN tabular prior reasoning for extreme micro-climates.
    """
    effective_temp = calculate_wind_chill(temp_celsius, wind_speed_kmh)
    
    # Rapid pressure drop indicator (e.g. > 3 hPa drop over 3 hours indicates incoming frontal storm)
    storm_prob = 10.0
    if pressure_delta_3h < -2.0:
        storm_prob += 40.0
    if pressure_delta_3h < -4.0:
        storm_prob += 35.0
    if humidity_percent > 80.0:
        storm_prob += 15.0
    storm_prob = min(98.0, max(5.0, storm_prob))

    # Hypothermia risk scoring
    # Wet clothes + wind at 5°C to 10°C is notoriously dangerous
    hypothermia_risk_score = 0.0
    if effective_temp <= 0.0:
        hypothermia_risk_score += 60.0
    elif effective_temp <= 10.0:
        hypothermia_risk_score += 35.0
    
    if humidity_percent > 75.0:
        hypothermia_risk_score += 25.0
    
    if elevation_meters > 2000.0:
        hypothermia_risk_score += 15.0

    hypothermia_prob = min(99.0, max(2.0, hypothermia_risk_score))

    # Overall Alert Classification
    if hypothermia_prob >= 75.0 or storm_prob >= 75.0:
        level = "CRITICAL"
        cue = "Urgent: Severe mountain microclimate shift detected. High hypothermia and storm probability. Seek immediate shelter."
    elif hypothermia_prob >= 45.0 or storm_prob >= 45.0:
        level = "ELEVATED"
        cue = "Caution: Deteriorating weather conditions. Equip thermal shell and prepare descent plan."
    else:
        level = "LOW_RISK"
        cue = "Trail climate stable. Enjoy the hike, stay hydrated, and monitor the horizon."

    return {
        "status": level,
        "effective_temp_c": effective_temp,
        "storm_probability_pct": round(storm_prob, 1),
        "hypothermia_risk_pct": round(hypothermia_prob, 1),
        "voice_alert": cue,
        "recommendations": [
            f"Perceived Wind Chill: {effective_temp}°C (Actual: {temp_celsius}°C)",
            f"Barometric 3h Trend: {pressure_delta_3h:+.1f} hPa ({'Rapid Drop - Storm Front' if pressure_delta_3h < -2.0 else 'Stable'})",
            f"Elevation Lapse Factor: At {elevation_meters:.0f}m, ambient air temperature decreases by ~6.5°C per 1,000m gained."
        ]
    }

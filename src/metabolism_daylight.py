"""
TrailEcho Alpine Daylight & Physiological Energy/Hydration Calculator.
Pure Python implementations of:
1. Solar Sunset Countdown & Headlamp Enforcement Horizon
2. Pandolf Metabolic Equation for backcountry energy/hydration requirements
"""

import math
import datetime
from typing import Dict, Any


def calculate_daylight_horizon(
    current_hour: float = 14.5,  # 2:30 PM
    sunset_hour: float = 18.75    # 6:45 PM
) -> Dict[str, Any]:
    """
    Computes remaining daylight, golden hour onset, and headlamp enforcement deadlines.
    """
    remaining_hours = max(0.0, sunset_hour - current_hour)
    hours_int = int(remaining_hours)
    minutes_int = int((remaining_hours - hours_int) * 60)

    # Status classification
    if remaining_hours <= 1.0:
        status = "CRITICAL_DUSK"
        voice_cue = f"Urgent: Sunset in {minutes_int} minutes. If you are not at camp, turn on your headlamp immediately and avoid ridge edges."
    elif remaining_hours <= 2.5:
        status = "GOLDEN_HOUR_WARNING"
        voice_cue = f"Daylight Advisory: {hours_int} hours and {minutes_int} minutes of sunlight remaining. Assess turnaround point now."
    else:
        status = "OPTIMAL_DAYLIGHT"
        voice_cue = f"Daylight ample: {hours_int} hours {minutes_int} minutes until dusk. Maintain pace."

    return {
        "status": status,
        "remaining_hours": round(remaining_hours, 2),
        "remaining_display": f"{hours_int}h {minutes_int}m",
        "headlamp_deadline": f"{int(sunset_hour - 0.5):02d}:{int(((sunset_hour - 0.5) % 1) * 60):02d}",
        "voice_cue": voice_cue
    }


def calculate_backcountry_metabolism(
    hiker_weight_kg: float,
    pack_weight_kg: float,
    distance_km: float,
    elevation_gain_m: float,
    temp_celsius: float
) -> Dict[str, Any]:
    """
    Estimates calorie expenditure and water replenishment using Pandolf/Margaria heuristics.
    """
    total_mass_kg = hiker_weight_kg + pack_weight_kg
    
    # Flat terrain work: ~0.9 kcal per kg per km
    flat_energy_kcal = total_mass_kg * distance_km * 0.95
    
    # Vertical ascent work: ~1.5 kcal per kg per 100m elevation gain
    ascent_energy_kcal = total_mass_kg * (elevation_gain_m / 100.0) * 1.55
    
    # Total calorie burn
    total_kcal = round(flat_energy_kcal + ascent_energy_kcal, 0)
    
    # Hydration requirements (baseline 0.5L/h + temperature evaporation index)
    estimated_hours = (distance_km / 3.8) + (elevation_gain_m / 350.0)
    sweat_rate_liters_per_hour = 0.55 + max(0.0, (temp_celsius - 15.0) * 0.035)
    total_water_liters = round(estimated_hours * sweat_rate_liters_per_hour, 1)
    
    # Electrolyte sodium baseline: ~500mg per liter of fluid sweat
    sodium_mg = int(total_water_liters * 500)

    voice_cue = f"Metabolic Plan: Projected burn {int(total_kcal)} calories. Minimum water requirement is {total_water_liters} liters with {sodium_mg} milligrams sodium electrolytes."

    return {
        "estimated_duration_hours": round(estimated_hours, 1),
        "total_calories_burned_kcal": int(total_kcal),
        "water_required_liters": total_water_liters,
        "sodium_electrolytes_mg": sodium_mg,
        "recommended_carbs_grams": int(total_kcal * 0.55 / 4.0),
        "voice_cue": voice_cue
    }

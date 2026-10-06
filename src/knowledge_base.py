"""
TrailEcho Wilderness Knowledge Base & Offline Fallback Matrices.
Ensures zero-connectivity trail safety for hikers, foragers, and campers.
"""

from typing import Dict, Any, List

# Curated offline wilderness survival matrices for zero-connectivity situations
OFFLINE_SURVIVAL_DATABASE: Dict[str, Dict[str, Any]] = {
    "hypothermia": {
        "title": "Hypothermia & Rapid Chill Protocol",
        "severity": "CRITICAL",
        "voice_alert": "Critical Alert: Hypothermia risk. Stop exposed movement. Put on waterproof thermal layers immediately. Sip warm liquids.",
        "action_steps": [
            "Get out of the wind and insulate from frozen or wet ground.",
            "Remove wet base layers and replace with dry wool or synthetic fleece.",
            "Cover head and neck (up to 40% heat loss area).",
            "Consume easily digestible high-calorie carbohydrates."
        ],
        "toxic_lookalikes": []
    },
    "death_cap": {
        "title": "Amanita phalloides (Death Cap Mushroom)",
        "severity": "LETHAL",
        "voice_alert": "Extreme Danger: Suspected Death Cap. Contains fatal amatoxins. Do not touch or ingest. One bite is lethal.",
        "action_steps": [
            "NEVER consume wild mushrooms with white gills, a membranous ring, and a bulbous cup/volva at the base.",
            "Wash hands thoroughly if touched.",
            "Do not store in the same container with edible mushrooms."
        ],
        "toxic_lookalikes": [
            "Edible Field Mushroom (Agaricus campestris) - Lookalike danger: Field mushrooms have pink-to-brown gills, never pure white."
        ]
    },
    "poison_ivy": {
        "title": "Toxicodendron radicans (Poison Ivy / Oak / Sumac)",
        "severity": "HIGH_IRRITANT",
        "voice_alert": "Urushiol Hazard: Leaves of three, let them be. Wash contacted skin with cold running water and soap within 15 minutes.",
        "action_steps": [
            "Remember the rule: 'Leaves of three, leave them be'.",
            "Wash skin with cold running water and dish soap/alcohol wipes to remove urushiol oil.",
            "Avoid burning the plant; inhaled smoke causes severe internal lung injury."
        ],
        "toxic_lookalikes": [
            "Virginia Creeper (Parthenocissus quinquefolia) - has 5 leaflets per stem rather than 3."
        ]
    },
    "snake_bite": {
        "title": "Pit Viper / Rattlesnake Envenomation",
        "severity": "CRITICAL",
        "voice_alert": "Emergency: Snake bite protocol. Keep limb still and below heart level. Remove rings or constrictive clothing. Do not cut or suck wound.",
        "action_steps": [
            "Keep the victim calm; elevated heart rate accelerates venom spread.",
            "Immobilize the bitten extremity at or slightly below heart level.",
            "DO NOT apply tourniquets, ice packs, or electrical shocks.",
            "DO NOT cut incisions or attempt oral suction."
        ],
        "toxic_lookalikes": []
    },
    "lightning_storm": {
        "title": "High-Altitude Lightning Storm Hazard",
        "severity": "CRITICAL",
        "voice_alert": "Storm Warning: Descend immediately from exposed ridges and peaks. Avoid isolated tall trees. Crouch on insulated pack.",
        "action_steps": [
            "Descend rapidly below the tree line and away from high ridges.",
            "Avoid open meadows, water bodies, and isolated tall trees.",
            "Adopt the lightning crouch: feet together, crouching low on your backpack or foam pad."
        ],
        "toxic_lookalikes": []
    }
}


def lookup_offline_emergency(keyword: str) -> Dict[str, Any]:
    """Find immediate offline triage knowledge when no network is available."""
    keyword_clean = keyword.lower().strip()
    for key, data in OFFLINE_SURVIVAL_DATABASE.items():
        if key in keyword_clean or keyword_clean in key:
            return data
    
    # Generic offline wilderness safety guidance
    return {
        "title": "General Wilderness Survival Priority (STOP Protocol)",
        "severity": "MODERATE",
        "voice_alert": "Stay calm. Follow the STOP rule: Sit down, Think, Observe your surroundings, and Plan before moving.",
        "action_steps": [
            "S - Stop and sit down. Panicking burns critical calories and leads to navigational errors.",
            "T - Think about your last known location, remaining daylight, and current supplies.",
            "O - Observe terrain, wind direction, water sources, and potential shelter.",
            "P - Plan your next moves: Shelter, Fire, Water, Signal."
        ],
        "toxic_lookalikes": []
    }

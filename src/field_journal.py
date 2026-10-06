"""
TrailEcho Offline Field Log & Backcountry Journal.
Allows hikers to cache voice notes, geo-tagged hazard observations,
and trail findings directly into local browser storage / exported JSON.
"""

from typing import List, Dict, Any
import datetime
import json


class TrailFieldJournal:
    """Manages offline hazard audit logs and trail waypoint observations."""

    def __init__(self):
        self.logs: List[Dict[str, Any]] = []

    def add_entry(
        self,
        topic: str,
        hazard_level: str,
        voice_cue: str,
        elevation: float,
        temp_c: float,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Creates a timestamped backcountry observation entry."""
        entry = {
            "id": f"log-{len(self.logs) + 1:03d}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "hazard_level": hazard_level,
            "voice_cue": voice_cue,
            "telemetry": {
                "elevation_m": elevation,
                "temp_c": temp_c
            },
            "field_notes": notes
        }
        self.logs.append(entry)
        return entry

    def export_json(self) -> str:
        """Exports all trail journal entries as structured JSON."""
        return json.dumps(self.logs, indent=2)

    def clear(self):
        """Clears in-memory journal logs."""
        self.logs = []


journal_singleton = TrailFieldJournal()

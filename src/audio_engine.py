"""
ElevenLabs Audio Synthesis Engine with Web Audio & Offline Fallback.
Enables screen-free outdoor interactions.
"""

import os
import requests
from typing import Optional, Tuple


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - Clear, calming wilderness guide voice


def synthesize_voice_alert(text: str, api_key: Optional[str] = None, voice_id: str = DEFAULT_VOICE_ID) -> Tuple[Optional[bytes], str]:
    """
    Synthesizes speech using ElevenLabs API.
    Returns: (audio_bytes, status_message)
    If API key is missing or quota exceeded, falls back gracefully.
    """
    key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not key or not key.strip():
        return None, "ElevenLabs API key not set. Using browser offline Web Speech API."

    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key.strip()
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.65,
            "similarity_boost": 0.8
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        if response.status_code == 200:
            return response.content, "Voice generated successfully with ElevenLabs."
        else:
            return None, f"ElevenLabs API returned {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return None, f"ElevenLabs synthesis failed: {str(e)}"

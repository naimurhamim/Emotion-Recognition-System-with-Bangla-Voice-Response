"""
Voice Engine — Microsoft Edge TTS
Voice: bn-BD-NabanitaNeural (default settings — best natural quality)
"""

import os
import uuid
import asyncio
import edge_tts

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")

VOICE  = "bn-BD-NabanitaNeural"
RATE   = "+0%"
PITCH  = "+0Hz"
VOLUME = "+10%"


def ensure_audio_dir():
    os.makedirs(AUDIO_DIR, exist_ok=True)


async def _generate(text: str, filepath: str):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        pitch=PITCH,
        volume=VOLUME,
    )
    await communicate.save(filepath)


def text_to_speech_bangla(text: str) -> str:
    ensure_audio_dir()
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    asyncio.run(_generate(text, filepath))
    return f"/static/audio/{filename}"


def cleanup_old_audio():
    ensure_audio_dir()
    for f in os.listdir(AUDIO_DIR):
        if f.endswith((".mp3", ".wav")):
            try:
                os.remove(os.path.join(AUDIO_DIR, f))
            except Exception:
                pass

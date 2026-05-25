from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

from emotion_engine import analyze_frames
from voice_engine import text_to_speech_bangla, cleanup_old_audio
from response_map import get_response

app = FastAPI(title="Emotion Recognition System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audio output folder
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount("/static/audio", StaticFiles(directory=AUDIO_DIR), name="audio")


class AnalyzeRequest(BaseModel):
    frames: List[str]
    user_name: str = "নাইমুর"


class AnalyzeResponse(BaseModel):
    dominant_emotion: str
    avg_scores: dict
    frame_count: int
    response_text: str
    audio_url: str


@app.get("/")
def root():
    return {"message": "Emotion Recognition API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if not req.frames:
        raise HTTPException(status_code=400, detail="No frames provided.")

    result   = analyze_frames(req.frames)
    dominant = result["dominant_emotion"]
    response_text = get_response(dominant, req.user_name)

    cleanup_old_audio()
    audio_url = text_to_speech_bangla(response_text)

    return AnalyzeResponse(
        dominant_emotion=dominant,
        avg_scores=result["avg_scores"],
        frame_count=result["frame_count"],
        response_text=response_text,
        audio_url=audio_url,
    )


@app.get("/emotions")
def list_emotions():
    return {
        "emotions": ["happy", "sad", "depressed", "angry", "surprised", "fear", "disgust", "neutral"]
    }

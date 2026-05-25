import cv2
import numpy as np
from deepface import DeepFace
from collections import Counter
import base64
import re


def decode_base64_image(b64_string: str) -> np.ndarray:
    """Decode a base64 image string to a numpy array (BGR)."""
    # Strip data URL prefix if present
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]
    img_bytes = base64.b64decode(b64_string)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img


def analyze_single_frame(img: np.ndarray) -> dict:
    """Run DeepFace emotion analysis on a single frame."""
    try:
        result = DeepFace.analyze(
            img_path=img,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )
        # result can be a list or dict depending on version
        if isinstance(result, list):
            result = result[0]
        emotions = result.get("emotion", {})
        dominant = result.get("dominant_emotion", max(emotions, key=emotions.get))
        return {"dominant": dominant, "scores": emotions, "error": None}
    except Exception as e:
        return {"dominant": "neutral", "scores": {}, "error": str(e)}


def analyze_frames(frames_b64: list[str]) -> dict:
    """
    Analyze multiple base64-encoded frames and return the most
    frequent dominant emotion along with aggregated scores.
    """
    dominants = []
    all_scores: dict[str, list[float]] = {}

    for b64 in frames_b64:
        img = decode_base64_image(b64)
        if img is None:
            continue
        res = analyze_single_frame(img)
        dominants.append(res["dominant"])
        for emotion, score in res["scores"].items():
            all_scores.setdefault(emotion, []).append(score)

    if not dominants:
        return {"dominant_emotion": "neutral", "avg_scores": {}, "frame_count": 0}

    # Most common dominant emotion across frames
    counter = Counter(dominants)
    final_dominant = counter.most_common(1)[0][0]

    # Average scores
    avg_scores = {e: round(sum(v) / len(v), 2) for e, v in all_scores.items()}

    return {
        "dominant_emotion": final_dominant,
        "avg_scores": avg_scores,
        "frame_count": len(dominants),
    }

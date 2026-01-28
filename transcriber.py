"""
transcriber.py
Uses OpenAI Whisper for speech-to-text.
GPU is used if available (RTX 3050 supported).
"""

import whisper
import torch

# Explicit GPU selection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Whisper running on:", DEVICE)

# Load whisper model on GPU
model = whisper.load_model("small", device=DEVICE)


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes a single audio chunk.
    Supports English, Telugu, Hindi and mixed language automatically.
    """

    result = model.transcribe(
        audio_path,
        fp16=(DEVICE == "cuda"),
        condition_on_previous_text=False
    )

    return result["text"]

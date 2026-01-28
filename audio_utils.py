"""
audio_utils.py
Handles audio preprocessing and chunking.
This ensures better transcription accuracy and performance.
"""

import ffmpeg
import os
import shutil


def preprocess_audio(input_audio: str) -> str:
    """
    Converts audio into clean WAV format:
    - Mono channel
    - 16kHz sample rate
    - Removes low & high frequency noise
    """

    if not os.path.exists(input_audio):
        raise FileNotFoundError("Audio file not found")

    output_audio = "clean_audio.wav"

    (
        ffmpeg
        .input(input_audio)
        .output(
            output_audio,
            ac=1,
            ar=16000,
            af="loudnorm,highpass=f=120,lowpass=f=4000"
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return output_audio


def split_audio(input_audio: str, chunk_minutes: int = 4):
    """
    Splits long audio into smaller chunks.
    Chunking is done internally and NOT shown to the user.
    """

    if os.path.exists("chunks"):
        shutil.rmtree("chunks")

    os.makedirs("chunks", exist_ok=True)

    chunk_seconds = chunk_minutes * 60
    output_pattern = "chunks/chunk_%03d.wav"

    (
        ffmpeg
        .input(input_audio)
        .output(
            output_pattern,
            f="segment",
            segment_time=chunk_seconds,
            ac=1,
            ar=16000
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return sorted(
        os.path.join("chunks", f)
        for f in os.listdir("chunks")
        if f.endswith(".wav")
    )

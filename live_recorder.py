"""
live_recorder.py
Live audio recording with manual stop option.
"""

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np


def record_audio(filename="lecture.wav", sample_rate=16000):
    """
    Records audio until user presses ENTER to stop.
    """

    print("Recording started...")
    print("Press ENTER to stop recording")

    frames = []

    def callback(indata, frames_count, time, status):
        frames.append(indata.copy())

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
        callback=callback
    ):
        input()   # waits for ENTER key

    # ---- FIX: handle empty recording ----
    if len(frames) == 0:
        print("No audio recorded. Please speak before stopping.")
        return

    audio = np.concatenate(frames, axis=0)
    write(filename, sample_rate, audio)

    print("Recording stopped and saved as", filename)

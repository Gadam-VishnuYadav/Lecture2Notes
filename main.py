import os
import shutil
import re
from dotenv import load_dotenv

# Project modules
from audio_utils import preprocess_audio, split_audio
from transcriber import transcribe_audio
from semantic_cleaner import semantic_clean
from notes_generator import generate_notes
from pdf_generator import create_pdf
from live_recorder import record_audio


# Load API keys
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("GROQ_API_KEY missing")
    exit(1)


# Only for user clarity
def choose_lecture_language():
    print("\nLecture language")
    print("1. English")
    print("2. Telugu")
    print("3. Hindi")
    print("4. Mixed")

    c = input("Choice: ").strip()

    if c == "1":
        return "English"
    if c == "2":
        return "Telugu"
    if c == "3":
        return "Hindi"
    return "Mixed"


# Create output folders
def make_folders():
    base = "outputs"
    os.makedirs(base, exist_ok=True)

    num = len(os.listdir(base)) + 1
    root = os.path.join(base, f"Lecture_{num}")

    audio = os.path.join(root, "audio")
    text = os.path.join(root, "transcript")
    pdf = os.path.join(root, "pdf")

    os.makedirs(audio)
    os.makedirs(text)
    os.makedirs(pdf)

    return audio, text, pdf, root


# Main pipeline
def run(audio_path):
    audio_dir, text_dir, pdf_dir, root = make_folders()

    # Preprocess audio
    clean_audio = preprocess_audio(audio_path)

    shutil.move(audio_path, os.path.join(audio_dir, "original.wav"))
    shutil.move(clean_audio, os.path.join(audio_dir, "clean.wav"))

    clean_audio = os.path.join(audio_dir, "clean.wav")

    # Split audio
    chunks = split_audio(clean_audio)

    # Transcription (multi-language)
    full_text = ""
    for c in chunks:
        full_text += transcribe_audio(c) + " "

    # Save transcript in paragraphs
    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    with open(
        os.path.join(text_dir, "transcript.txt"),
        "w",
        encoding="utf-8"
    ) as f:
        count = 0
        for s in sentences:
            s = s.strip()
            if not s:
                continue

            f.write(s + "\n")
            count += 1

            # New paragraph after 4 sentences
            if count % 4 == 0:
                f.write("\n")

    # Clean transcript
    cleaned = semantic_clean(full_text)

    # Estimate duration
    words = len(cleaned.split())
    minutes = max(10, words // 140)

    # Notes generation
    topic = input("\nTopic name: ").strip()
    notes = generate_notes(cleaned, minutes, "English")

    # PDF creation
    pdf_path = create_pdf(notes, topic, pdf_dir)

    print("\nFinished")
    print("Folder:", root)
    print("PDF:", pdf_path)


# Entry point
if __name__ == "__main__":
    print("Lecture voice to notes")
    print("1. Audio file")
    print("2. Live recording")

    choice = input("Choice: ").strip()

    choose_lecture_language()  # informational only

    if choice == "1":
        path = input("Audio file path: ").strip()
        run(path)

    elif choice == "2":
        record_audio()
        run("lecture.wav")

    else:
        print("Invalid option")

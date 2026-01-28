
---

# Lecture2Notes

Lecture2Notes is an AI-powered tool that converts lecture audio into clear, well-structured study notes. It supports multiple languages, handles real classroom audio, and produces clean, exam-ready PDF notes automatically.

---

## Features

* **Multi-Language Lectures**
  Supports English, Telugu, Hindi, and mixed-language lectures.

* **AI-Based Note Generation**
  Uses Groq AI to generate detailed, structured academic notes instead of short summaries.

* **Professional PDF Output**
  Automatically creates clean, properly formatted PDFs suitable for studying and revision.

* **Audio Preprocessing**
  Improves transcription accuracy using noise reduction and audio optimization.

* **Web Application**
  Simple and intuitive Streamlit-based interface for uploading audio and generating notes.

* **Command-Line Tool**
  Terminal version with support for both file uploads and live lecture recording.

---

## Demo

### Web Interface (Streamlit)

* Upload lecture audio files
* Select lecture language
* Generate AI-based notes
* Download a professional PDF

### Command-Line Version

* Upload existing audio files or record live lectures
* Automatic multi-language transcription
* Fully automated notes generation

---

## Installation

### Prerequisites

* Python 3.8 or higher
* **FFmpeg (Required)** – must be installed before running the project

---

### Step 1: Install FFmpeg

FFmpeg is required for audio preprocessing.

**Windows**

```bash
# Using Chocolatey (recommended)
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
# Make sure FFmpeg is added to PATH
```

**macOS**

```bash
brew install ffmpeg
```

**Linux (Ubuntu / Debian)**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation**

```bash
ffmpeg -version
```

---

### Step 2: Clone and Set Up the Project

1. Clone the repository:

```bash
git clone https://github.com/yourusername/lecture2notes.git
cd lecture2notes
```

2. Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

* **Windows**

```bash
venv\Scripts\activate
```

* **macOS / Linux**

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key.
Get a free key from: [https://console.groq.com/keys](https://console.groq.com/keys)

---

## Usage

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Open your browser at:
`http://localhost:8501`

Steps:

1. Upload a lecture audio file (WAV, MP3, MP4, M4A, OGG)
2. Select lecture language
3. Enter the topic name
4. Click **Generate Notes**
5. Download the generated PDF

---

### Command-Line Interface

```bash
python main.py
```

Options:

1. Upload an existing audio file
2. Record a lecture live (press **ENTER** to stop recording)

---

## Project Structure

```
lecture2notes/
├── app.py                 # Streamlit web interface
├── main.py                # Command-line interface
├── audio_utils.py         # Audio preprocessing and chunking
├── transcriber.py         # Whisper-based transcription
├── semantic_cleaner.py    # Transcript cleaning
├── notes_generator.py     # AI notes generation (Groq)
├── pdf_generator.py       # PDF creation
├── live_recorder.py       # Live audio recording (CLI)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── README.md              # Documentation
```

---

## How It Works

1. **Audio Preprocessing**
   Converts audio to a clean 16kHz mono format with noise reduction.

2. **Chunking**
   Splits long audio into smaller chunks for better transcription.

3. **Transcription**
   Uses OpenAI Whisper for accurate multi-language speech-to-text.

4. **Cleaning**
   Removes filler words and broken sentences without changing meaning.

5. **AI Notes Generation**
   Groq LLaMA 3.1 generates detailed, structured academic notes.

6. **PDF Creation**
   Notes are converted into a professionally formatted PDF.

---

## Supported Languages

* **Transcription**: English, Telugu, Hindi, Mixed Languages
* **Notes Output**: English

---

## Configuration

### Notes Length

Notes length is automatically adjusted based on lecture duration:

* Up to 10 minutes → ~1500 words
* Up to 30 minutes → ~3000 words
* More than 30 minutes → ~4500+ words

---

### Supported Audio Formats

WAV, MP3, MP4, M4A, OGG

---

## Output Structure

```
outputs/
└── Lecture_1/
    ├── audio/
    │   ├── original.wav
    │   └── clean.wav
    ├── transcript/
    │   └── transcript.txt
    └── pdf/
        └── Topic_Name.pdf
```

---

## Requirements

* Python 3.8 or higher
* FFmpeg
* Groq API key (free)
* CUDA-compatible GPU (optional, improves transcription speed)

---

## API Key Setup

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Create an account
3. Generate an API key
4. Add it to `.env`:

```
GROQ_API_KEY=your_api_key_here
```

---

## Troubleshooting

### FFmpeg Not Found

* Ensure FFmpeg is installed and added to PATH
* Restart your terminal after installation

### CUDA Errors

* Whisper automatically falls back to CPU if no GPU is available

### API Errors

* Check that your Groq API key is valid
* Ensure you have internet access
* Confirm you are within API limits

### Audio Quality Issues

* Use clear recordings with minimal background noise
* Ensure speaker volume is sufficient

---

## Performance

* **CPU Mode**: ~5–10 minutes per hour of audio
* **GPU Mode**: ~1–2 minutes per hour (RTX 3050 or better)

---

## Contributing

Contributions are welcome.
Feel free to open an issue or submit a pull request.

---

## Acknowledgments

* OpenAI Whisper – speech-to-text
* Groq – AI note generation
* Streamlit – web interface
* ReportLab – PDF generation

---

## Roadmap

* [ ] Additional output languages
* [ ] Custom note templates
* [ ] Batch processing
* [ ] Video file support
* [ ] Cloud deployment
* [ ] Mobile application

---

**Note:**
Live recording is available only in the command-line version (`main.py`).
The web interface (`app.py`) supports file uploads only.

---

If you want, I can now:

* Make this **resume-friendly**
* Shorten it for **GitHub front page**
* Or rewrite it in **academic / startup / student tone**

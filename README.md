# Lecture2Notes

Transform lecture audio into professional study notes using AI. Supports multiple languages and generates well-structured PDF notes automatically.

## Features

- **Multi-Language Support**: English, Telugu, Hindi, and mixed language lectures
- **AI-Powered Notes**: Generates detailed, structured academic notes using Groq AI
- **Professional PDF Output**: Clean, formatted PDFs ready for studying
- **Audio Preprocessing**: Automatic noise reduction and optimization
- **Web Interface**: Easy-to-use Streamlit web application
- **Command Line Tool**: Terminal version with live recording support

## Demo

### Web Interface (Streamlit)
- Upload audio files
- Select lecture and notes language
- Generate AI-powered notes
- Download professional PDF

### Terminal Version
- Upload audio files OR record live lectures
- Multi-language transcription
- Automated notes generation

## Installation

### Prerequisites
- Python 3.8 or higher
- **FFmpeg (Required)** - Must be installed first

### Step 1: Install FFmpeg

FFmpeg is required for audio processing. Install it before running the application:

**Windows:**
```bash
# Using chocolatey (recommended)
choco install ffmpeg

# Or download installer from https://ffmpeg.org/download.html
# Add FFmpeg to your system PATH after installation
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

### Step 2: Clone and Setup Project

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lecture2notes.git
cd lecture2notes
```

2. Create virtual environment:
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
# Get free API key from: https://console.groq.com/keys
```

## Usage

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

1. Upload your lecture audio file (WAV, MP3, MP4, M4A, OGG)
2. Select lecture language
3. Enter topic name
4. Click "Generate Notes"
5. Download the generated PDF

### Command Line Interface

```bash
python main.py
```

Options:
1. **Upload Audio File**: Process existing audio files
2. **Live Recording**: Record lecture in real-time (press ENTER to stop)

## Project Structure

```
lecture2notes/
├── app.py                 # Streamlit web interface
├── main.py                # Command line interface
├── audio_utils.py         # Audio preprocessing and chunking
├── transcriber.py         # Whisper-based transcription
├── semantic_cleaner.py    # Transcript cleaning
├── notes_generator.py     # AI notes generation (Groq)
├── pdf_generator.py       # PDF creation
├── live_recorder.py       # Live audio recording
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Documentation
```

## How It Works

1. **Audio Preprocessing**: Converts audio to optimal format (16kHz, mono, noise-reduced)
2. **Chunking**: Splits long audio into manageable chunks
3. **Transcription**: Uses OpenAI Whisper for accurate multi-language transcription
4. **Cleaning**: Removes filler words and formatting issues
5. **AI Notes Generation**: Groq LLaMA 3.1 creates structured academic notes
6. **PDF Creation**: Generates professional PDF with proper formatting

## Supported Languages

- **Transcription**: English, Telugu, Hindi, Mixed Languages
- **Notes Output**: English

## Configuration

### Notes Length

The AI automatically adjusts notes length based on lecture duration:
- ≤10 minutes: ~1500 words
- ≤30 minutes: ~3000 words
- >30 minutes: ~4500+ words

### Audio Formats

Supported formats: WAV, MP3, MP4, M4A, OGG

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

## Requirements

- Python 3.8+
- FFmpeg
- CUDA-compatible GPU (optional, for faster transcription)
- Groq API key (free)

## API Key Setup

1. Visit [Groq Console](https://console.groq.com/keys)
2. Create a free account
3. Generate an API key
4. Add to `.env` file:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Troubleshooting

### FFmpeg not found
- Ensure FFmpeg is installed and in your system PATH
- Restart your terminal after installation

### CUDA errors
- If you don't have a GPU, Whisper will automatically use CPU
- GPU provides faster transcription but is not required

### API errors
- Verify your Groq API key is correct in `.env`
- Check your internet connection
- Ensure you haven't exceeded API rate limits

### Audio quality issues
- Use high-quality audio recordings
- Minimize background noise
- Ensure speaker volume is adequate

## Performance

- **CPU Mode**: ~5-10 minutes per hour of audio
- **GPU Mode**: ~1-2 minutes per hour of audio (RTX 3050 or better)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenAI Whisper for transcription
- Groq for AI notes generation
- Streamlit for web interface
- ReportLab for PDF generation

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [ ] More output languages
- [ ] Custom note templates
- [ ] Batch processing
- [ ] Video file support
- [ ] Cloud deployment
- [ ] Mobile app

---

**Note**: Live recording is only available in the command-line version (`main.py`). The web interface (`app.py`) supports file uploads only.

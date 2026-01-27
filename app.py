import streamlit as st
import os
import shutil
import re
from dotenv import load_dotenv
import tempfile

# Project modules
from audio_utils import preprocess_audio, split_audio
from transcriber import transcribe_audio
from semantic_cleaner import semantic_clean
from notes_generator import generate_notes
from pdf_generator import create_pdf

# Load API keys
load_dotenv()

# Page config
st.set_page_config(page_title="Lecture2Notes", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS - Premium Red-White-Glass Design
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Header styling - REDUCED SIZE */
    .main-header {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        padding: 1.2rem 2rem;
        border-radius: 0;
        color: white;
        text-align: left;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
        opacity: 0.95;
        font-weight: 400;
    }
    
    /* Glass effect panels */
    .glass-panel {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(220, 38, 38, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }
    
    /* HIDE EMPTY WHITE BOXES */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    /* Remove extra spacing */
    .element-container:has(> div:empty) {
        display: none !important;
    }
    
    /* Compact sections */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(220, 38, 38, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #991b1b 0%, #7f1d1d 100%);
        box-shadow: 0 6px 12px rgba(220, 38, 38, 0.3);
        transform: translateY(-2px);
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.9);
        border: 2px dashed rgba(220, 38, 38, 0.3);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-weight: 500;
        color: #1f2937;
        font-size: 1rem;
    }
    
    /* Radio button circles - white background */
    .stRadio > div {
        background-color: white;
    }
    
    .stRadio > div > label > div[data-baseweb="radio"] > div {
        background-color: white !important;
        border: 2px solid rgba(220, 38, 38, 0.3) !important;
    }
    
    .stRadio > div > label > div[data-baseweb="radio"] > div:first-child {
        background-color: white !important;
    }
    
    /* Selected radio button */
    .stRadio > div > label > div[data-baseweb="radio"] > div[data-testid="stMarkdownContainer"] {
        color: #1f2937 !important;
    }
    
    /* Radio text visibility */
    .stRadio label {
        color: #1f2937 !important;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        border: 2px solid rgba(220, 38, 38, 0.2);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #dc2626;
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
    }
    
    /* Text area - FORCE WHITE BACKGROUND */
    .stTextArea > div > div > textarea {
        border: 2px solid rgba(220, 38, 38, 0.2) !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #fbbf24;
        border-radius: 8px;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 4px 6px rgba(5, 150, 105, 0.2);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%);
        box-shadow: 0 6px 12px rgba(5, 150, 105, 0.3);
        transform: translateY(-2px);
    }
    
    /* Section headers */
    h2, h3 {
        color: #1f2937;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #dc2626;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #dc2626 !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Lecture2Notes</h1>
    <p>Capture Every Lecture Instantly | Any Language | AI-Powered Smart Notes</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'notes_generated' not in st.session_state:
    st.session_state.notes_generated = False
if 'generated_notes' not in st.session_state:
    st.session_state.generated_notes = ""
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'transcript_text' not in st.session_state:
    st.session_state.transcript_text = ""

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

# Main processing function
def process_audio(audio_path, topic_name, output_language):
    audio_dir, text_dir, pdf_dir, root = make_folders()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Preprocess audio
        status_text.text("Preprocessing audio...")
        progress_bar.progress(10)
        clean_audio = preprocess_audio(audio_path)
        
        shutil.copy(audio_path, os.path.join(audio_dir, "original.wav"))
        shutil.move(clean_audio, os.path.join(audio_dir, "clean.wav"))
        clean_audio = os.path.join(audio_dir, "clean.wav")
        
        # Split audio
        status_text.text("Splitting audio into chunks...")
        progress_bar.progress(20)
        chunks = split_audio(clean_audio)
        
        # Transcription
        status_text.text("Transcribing audio...")
        full_text = ""
        chunk_progress = 20
        
        for i, c in enumerate(chunks):
            full_text += transcribe_audio(c) + " "
            chunk_progress = 20 + int((i + 1) / len(chunks) * 40)
            progress_bar.progress(chunk_progress)
        
        # Save transcript
        status_text.text("Saving transcript...")
        progress_bar.progress(65)
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        with open(os.path.join(text_dir, "transcript.txt"), "w", encoding="utf-8") as f:
            count = 0
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                f.write(s + "\n")
                count += 1
                if count % 4 == 0:
                    f.write("\n")
        
        st.session_state.transcript_text = full_text
        
        # Clean transcript
        status_text.text("Cleaning transcript...")
        progress_bar.progress(75)
        cleaned = semantic_clean(full_text)
        
        # Estimate duration
        words = len(cleaned.split())
        minutes = max(10, words // 140)
        
        # Generate notes
        status_text.text("Generating notes with AI...")
        progress_bar.progress(85)
        notes = generate_notes(cleaned, minutes, output_language)
        st.session_state.generated_notes = notes
        
        # Create PDF
        status_text.text("Creating PDF...")
        progress_bar.progress(95)
        pdf_path = create_pdf(notes, topic_name, pdf_dir)
        st.session_state.pdf_path = pdf_path
        
        progress_bar.progress(100)
        status_text.text("Complete!")
        
        return notes, pdf_path, root
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None, None

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    # Input method
    st.subheader("Choose File")
    
    audio_file = st.file_uploader("", type=['wav', 'mp3', 'mp4', 'm4a', 'ogg'], label_visibility="collapsed")
    
    # Language selection
    st.subheader("Choose Lecture Language")
    lecture_lang_options = ["ENGLISH", "TELUGU", "HINDI", "BLENDED LANGUAGE"]
    lecture_lang = st.radio("", lecture_lang_options, label_visibility="collapsed")
    
    st.subheader("Choose Notes Language")
    notes_lang = st.radio("", ["ENGLISH"], label_visibility="collapsed")
    
    # Topic input - NO GLASS PANEL
    topic_name = st.text_input("Topic Name", placeholder="Enter topic name...")
    
    # Generate button
    if st.button("Generate Notes"):
        if not os.getenv("GROQ_API_KEY"):
            st.error("GROQ_API_KEY is missing. Please add it to your .env file.")
        elif not topic_name:
            st.warning("Please enter a topic name.")
        elif not audio_file:
            st.warning("Please upload an audio file.")
        else:
            with st.spinner("Processing..."):
                # Save uploaded file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_file.read())
                    temp_path = tmp_file.name
                
                notes, pdf_path, root = process_audio(temp_path, topic_name, notes_lang)
                
                if notes and pdf_path:
                    st.session_state.notes_generated = True
                    st.success("Notes generated successfully!")

with col2:
    # Notes preview
    st.subheader("Notes Preview")
    
    if st.session_state.notes_generated and st.session_state.generated_notes:
        # Display notes in text area
        st.text_area("", value=st.session_state.generated_notes, height=500, label_visibility="collapsed")
    else:
        st.info("Notes will appear here after generation.")
    
    # Download button
    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        with open(st.session_state.pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Pdf",
                data=pdf_file,
                file_name=os.path.basename(st.session_state.pdf_path),
                mime="application/pdf"
            )

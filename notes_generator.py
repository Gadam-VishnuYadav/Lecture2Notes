"""
notes_generator.py
Generates very detailed and understandable academic lecture notes
using Groq API (LLaMA 3.1 – stable free model).
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_notes(clean_text, minutes, output_language):
    """
    Generates very detailed, structured, and understandable academic notes.
    Includes introduction, detailed explanation, applications,
    advantages, and disadvantages (only if relevant).
    """

    if not clean_text or not clean_text.strip():
        raise ValueError("Transcript is empty. Cannot generate notes.")

    # Decide depth based on lecture duration
    if minutes <= 10:
        depth = "at least 1500 words"
    elif minutes <= 30:
        depth = "at least 3000 words"
    else:
        depth = "at least 4500 words"

    prompt = f"""
Generate VERY DETAILED and EASY-TO-UNDERSTAND academic lecture notes
from the lecture transcript given below.

STRICT RULES:
- Do NOT summarize the lecture
- Explain concepts clearly as if teaching a beginner
- Use simple academic English suitable for students
- Do not use roman numerals anywhere
- Use proper headings and sub-headings
- Start each paragraph with a complete sentence
- Leave a blank line between sections for readability

MANDATORY STRUCTURE:

Introduction
- Clearly introduce the topic
- Explain the importance of the topic
- Give an overview of what the lecture covers

Detailed Explanation
- Break the topic into logical subtopics
- Explain each subtopic step by step
- Use clear sub-headings
- Do not skip explanations

Examples
- Provide simple and relevant examples
- Help students understand concepts practically

Applications
- Include applications only if relevant
- Explain where and how the topic is used in real life or academics

Advantages and Disadvantages
- Include only if meaningful
- Explain each advantage and disadvantage clearly

Conclusion / Quick Revision Summary
- End with a short recap for exam revision

LENGTH REQUIREMENT:
- Write {depth}
- Expand explanations instead of shortening content
- Do not intentionally limit content length

LANGUAGE:
- Write the notes in {output_language}

LECTURE TRANSCRIPT:
{clean_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1024  # SAFE limit to avoid Groq errors
        )
    except Exception as e:
        raise RuntimeError(f"Groq API request failed: {e}")

    notes = response.choices[0].message.content

    if not notes or not notes.strip():
        raise RuntimeError("Groq did not return any content.")

    return notes

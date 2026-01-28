"""
pdf_generator.py
Creates professional academic PDFs with automatic formatting.
Adapts to any content structure with proper alignment, headings, and spacing.
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def clean_filename(text):
    """Make filename safe for OS"""
    text = re.sub(r"[^\w\s-]", "", text)
    return text.strip().replace(" ", "_")


def clean_text(line):
    """Remove unwanted symbols and normalize text"""
    # Remove markdown and special symbols
    line = re.sub(r"[•*#>`~\[\]{}\\]", "", line)
    
    # Fix common formatting issues
    line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)  # Remove ** bold markers
    line = re.sub(r"__(.+?)__", r"\1", line)  # Remove __ bold markers
    line = re.sub(r"_{2,}", "", line)  # Remove multiple underscores
    line = re.sub(r"-{3,}", "", line)  # Remove horizontal rules
    
    # Normalize spaces
    line = re.sub(r"\s+", " ", line).strip()
    
    return line


def detect_line_type(line, prev_line=""):
    """
    Detect what type of content this line is:
    - main_heading: Main section heading
    - sub_heading: Sub-section heading  
    - numbered: Numbered list item
    - bullet: Bullet point
    - example: Example or case
    - paragraph: Regular paragraph text
    """
    
    if not line:
        return "empty"
    
    line_lower = line.lower().strip()
    
    # Main headings (Introduction, Definition, etc.)
    main_headings = [
        "introduction", "definition", "explanation", "working",
        "advantages", "disadvantages", "applications", "conclusion",
        "examples", "types", "overview", "summary", "features",
        "characteristics", "properties", "benefits", "limitations",
        "use cases", "methodology", "implementation", "description",
        "lecture notes", "background", "theory", "concept"
    ]
    
    for heading in main_headings:
        if line_lower == heading or line_lower == heading + ":":
            return "main_heading"
        if line_lower.startswith(heading + ":") or line_lower.startswith(heading + " -"):
            return "main_heading"
    
    # Numbered items (1. 2. 3. or 1) 2) 3))
    if re.match(r'^\d+[\.)]\s+', line):
        return "numbered"
    
    # Bullet points
    if re.match(r'^[-•○●]\s+', line):
        return "bullet"
    
    # Sub-headings (contains colon, relatively short, not a list item)
    if ":" in line and len(line.split()) <= 8 and not re.match(r'^\d+[\.)]\s+', line):
        return "sub_heading"
    
    # Examples or labeled items
    if line_lower.startswith(("example", "case", "note:", "important:")):
        return "example"
    
    # Regular paragraph
    return "paragraph"


def is_complete_sentence(line):
    """Check if sentence is reasonably complete"""
    # Very short lines are likely incomplete
    if len(line.split()) < 4:
        return False
    
    # Check for obvious incomplete endings
    incomplete_patterns = [
        r'\s(and|or|but|with|from|to|for|in|of|a|an|the)$',
        r'\s(according to|such as|including|related to|defined as|is a|are)$',
        r'^(According to|Such as|Including)\s*$'
    ]
    
    for pattern in incomplete_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return False
    
    return True


def wrap_text(text, font_name, font_size, max_width, pdf_canvas):
    """Wrap text to fit within max_width"""
    return simpleSplit(text, font_name, font_size, max_width)


def draw_justified_text(pdf, text, x, y, max_width, font_name, font_size, justify=True):
    """Draw text with justification"""
    words = text.split()
    
    if len(words) == 0:
        return y
    
    # Calculate if text fits in one line
    text_width = pdf.stringWidth(text, font_name, font_size)
    
    if text_width <= max_width:
        pdf.drawString(x, y, text)
        return y - (font_size + 6)
    
    # Multi-line wrapping
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = pdf.stringWidth(test_line, font_name, font_size)
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(current_line)
            current_line = [word]
    
    if current_line:
        lines.append(current_line)
    
    # Draw lines with optional justification
    for i, line_words in enumerate(lines):
        is_last_line = (i == len(lines) - 1)
        
        if not justify or is_last_line or len(line_words) == 1:
            # Left align
            pdf.drawString(x, y, ' '.join(line_words))
        else:
            # Justify
            line_text = ' '.join(line_words)
            text_width = pdf.stringWidth(line_text, font_name, font_size)
            num_gaps = len(line_words) - 1
            
            if num_gaps > 0:
                extra_space = (max_width - text_width) / num_gaps
                current_x = x
                
                for j, word in enumerate(line_words):
                    pdf.drawString(current_x, y, word)
                    word_width = pdf.stringWidth(word, font_name, font_size)
                    
                    if j < num_gaps:
                        space_width = pdf.stringWidth(' ', font_name, font_size)
                        current_x += word_width + space_width + extra_space
            else:
                pdf.drawString(x, y, line_text)
        
        y -= (font_size + 6)
    
    return y


def create_pdf(notes, topic_name, pdf_dir):
    """Generate professional PDF with automatic formatting"""
    
    filename = clean_filename(topic_name) + ".pdf"
    pdf_path = os.path.join(pdf_dir, filename)

    pdf = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Page setup
    left_margin = 72
    right_margin = 72
    top_margin = 72
    bottom_margin = 72
    
    max_width = width - left_margin - right_margin
    x = left_margin
    y = height - top_margin

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    title_clean = clean_text(topic_name.upper())
    pdf.drawCentredString(width / 2, y, title_clean)
    y -= 45

    # Process content
    lines = notes.split("\n")
    prev_line_type = None
    
    for raw_line in lines:
        line = clean_text(raw_line)
        
        if not line:
            y -= 8
            continue
        
        # Detect line type
        line_type = detect_line_type(line)
        
        # Page break check
        min_space = 100 if line_type in ["main_heading", "sub_heading"] else 60
        if y < bottom_margin + min_space:
            pdf.showPage()
            y = height - top_margin
            pdf.setFont("Helvetica", 11)
        
        # Main Heading
        if line_type == "main_heading":
            # Add space before heading
            if prev_line_type not in [None, "main_heading"]:
                y -= 12
            
            pdf.setFont("Helvetica-Bold", 14)
            heading_text = line.rstrip(":").strip()
            heading_text = heading_text.title() if not heading_text.isupper() else heading_text
            heading_text += ":"
            
            pdf.drawString(x, y, heading_text)
            y -= 28
            pdf.setFont("Helvetica", 11)
        
        # Sub-heading
        elif line_type == "sub_heading":
            y -= 8
            pdf.setFont("Helvetica-Bold", 12)
            
            sub_heading_text = line if line.endswith(":") else line + ":"
            pdf.drawString(x, y, sub_heading_text)
            y -= 22
            pdf.setFont("Helvetica", 11)
        
        # Numbered item
        elif line_type == "numbered":
            match = re.match(r'^(\d+[\.)]\s+)(.+)$', line)
            if match:
                number = match.group(1)
                text = match.group(2).strip()
                
                # Validate content
                if not is_complete_sentence(text):
                    continue
                
                # Add period if missing
                if text[-1] not in ".!?":
                    text += "."
                
                pdf.setFont("Helvetica", 11)
                pdf.drawString(x, y, number)
                
                number_width = pdf.stringWidth(number, "Helvetica", 11)
                indent_x = x + number_width
                indent_width = max_width - number_width
                
                y = draw_justified_text(pdf, text, indent_x, y, indent_width, "Helvetica", 11, justify=True)
                y -= 4
        
        # Bullet point
        elif line_type == "bullet":
            text = re.sub(r'^[-•○●]\s+', '', line).strip()
            
            if not is_complete_sentence(text):
                continue
            
            if text[-1] not in ".!?":
                text += "."
            
            pdf.setFont("Helvetica", 11)
            pdf.drawString(x, y, "• ")
            
            bullet_width = pdf.stringWidth("• ", "Helvetica", 11)
            indent_x = x + bullet_width + 5
            indent_width = max_width - bullet_width - 5
            
            y = draw_justified_text(pdf, text, indent_x, y, indent_width, "Helvetica", 11, justify=True)
            y -= 4
        
        # Example or special note
        elif line_type == "example":
            pdf.setFont("Helvetica-Oblique", 11)
            
            if line[-1] not in ".!?:":
                line += ":"
            
            y = draw_justified_text(pdf, line, x, y, max_width, "Helvetica-Oblique", 11, justify=False)
            y -= 2
            pdf.setFont("Helvetica", 11)
        
        # Regular paragraph
        else:
            # Skip incomplete sentences
            if not is_complete_sentence(line):
                continue
            
            # Add period if missing
            if line[-1] not in ".!?":
                line += "."
            
            pdf.setFont("Helvetica", 11)
            y = draw_justified_text(pdf, line, x, y, max_width, "Helvetica", 11, justify=True)
            y -= 6
        
        prev_line_type = line_type

    pdf.save()
    return pdf_path
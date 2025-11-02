import google.generativeai as genai
import time
import re
from pathlib import Path
from config import *

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_ai_correction_prompt():
    """
    Returns comprehensive prompt for OCR correction and Markdown conversion
    """
    return """
You are a professional text correction and formatting specialist. Convert this scanned book page into perfect Markdown format.

**CRITICAL TASKS:**

1. **OCR ERROR CORRECTION:**
   - Fix all spelling mistakes from OCR errors
   - Correct misplaced characters (e.g., 'rn' → 'm', 'cl' → 'd')
   - Fix French accent errors (e.g., 'a' → 'à', 'e' → 'é')
   - Correct word segmentation errors

2. **MARKDOWN FORMATTING:**
   - Preserve the EXACT document structure and hierarchy
   - Use proper heading levels (#, ##, ###)
   - Format book titles in italics: *Titre du Livre*
   - Maintain lists, bullet points, and numbered items
   - Keep paragraph breaks natural
   - Preserve publication metadata and author information

3. **FRENCH LANGUAGE SPECIFICS:**
   - Ensure proper French grammar and punctuation
   - Maintain French quotation marks: « ... »
   - Keep French formatting conventions
   - Preserve academic and scientific terminology

4. **DOCUMENT STRUCTURE:**
   - Maintain original page flow and logical sections
   - Keep figure references and captions
   - Preserve bibliographic citations
   - Maintain the author's writing style

**ORIGINAL TEXT:**
{text}

**IMPORTANT:** Return ONLY the corrected Markdown text, no explanations or notes.
"""

def process_pdf_to_markdown(pdf_path, part_number, total_parts):
    """
    Process a PDF part to corrected Markdown using AI
    """
    print(f"🤖 Processing part {part_number}/{total_parts}: {pdf_path.name}")
    
    for attempt in range(MAX_RETRIES):
        try:
            # Upload PDF to Gemini
            uploaded_file = genai.upload_file(pdf_path)
            
            # Generate content with correction prompt
            prompt = get_ai_correction_prompt()
            response = model.generate_content([prompt, uploaded_file])
            
            # Clean up the response
            markdown_text = response.text.strip()
            
            # Remove any potential AI intro/outro text
            markdown_text = re.sub(r'^```markdown\s*', '', markdown_text)
            markdown_text = re.sub(r'\s*```$', '', markdown_text)
            
            print(f"✅ Successfully processed part {part_number}")
            return markdown_text
            
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed for {pdf_path.name}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"❌ Failed to process {pdf_path.name} after {MAX_RETRIES} attempts")
                return None

def convert_all_parts_to_markdown(input_dir=CLEANED_PARTS_DIR):
    """
    Convert all cleaned PDF parts to Markdown
    """
    pdf_files = sorted(
        input_dir.glob("*.pdf"), 
        key=lambda f: int(''.join(filter(str.isdigit, f.stem)))
    )
    total_parts = len(pdf_files)
    
    all_markdown = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        markdown_content = process_pdf_to_markdown(pdf_file, i, total_parts)
        
        if markdown_content:
            # Add part separator
            all_markdown.append(f"\n\n---\n## Partie {i}\n\n")
            all_markdown.append(markdown_content)
        
        # Rate limiting
        time.sleep(2)
    
    return "".join(all_markdown)

def save_final_markdown(markdown_content, filename=FINAL_OUTPUT):
    """
    Save the complete Markdown content to file
    """
    output_path = MARKDOWN_OUTPUT_DIR / filename
    output_path.write_text(markdown_content, encoding=OUTPUT_ENCODING)
    print(f"💾 Final Markdown saved to: {output_path}")
    return output_path
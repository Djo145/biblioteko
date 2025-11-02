# Configuration settings
import os
from pathlib import Path

# API Configuration
api_key_path = Path(__file__).parent / "apikey.txt"
with open(api_key_path, "r") as f:
    API_KEY = f.read().strip()

# Processing settings
CHUNK_SIZE = 10  # Pages per chunk
OCR_DPI = 300
OUTPUT_ENCODING = "utf-8"

# Paths
RAW_PARTS_DIR = Path("pdf_processed_output/raw_parts")
CLEANED_PARTS_DIR = Path("pdf_processed_output/cleaned_parts")
FORMATTED_PARTS_DIR = Path("pdf_processed_output/formatted_parts")      
MARKDOWN_OUTPUT_DIR = Path("pdf_processed_output/markdown_output")
FINAL_OUTPUT = "final_book.md"

# AI Settings
MODEL_NAME = "gemini-2.5-flash"  # or "gemini-2.0-flash"
MAX_RETRIES = 3
RETRY_DELAY = 5

# Create directories
for directory in [RAW_PARTS_DIR, CLEANED_PARTS_DIR, MARKDOWN_OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)
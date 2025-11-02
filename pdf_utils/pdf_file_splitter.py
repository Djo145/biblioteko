import os
import PyPDF2
from pathlib import Path
from config import RAW_PARTS_DIR, CHUNK_SIZE

def split_pdf(input_path, n=CHUNK_SIZE, output_dir=RAW_PARTS_DIR):
    """
    Split a large PDF into smaller chunks for processing
    """
    print(f"📂 Splitting PDF: {input_path} into chunks of {n} pages...")
    
    os.makedirs(output_dir, exist_ok=True)
    reader = PyPDF2.PdfReader(input_path)
    total_pages = len(reader.pages)
    
    chunks_created = 0
    for i in range(0, total_pages, n):
        writer = PyPDF2.PdfWriter()
        chunk_pages = reader.pages[i:i+n]
        
        for page in chunk_pages:
            writer.add_page(page)
            
        part_path = output_dir / f"part_{i//n+1:03d}.pdf"
        with open(part_path, "wb") as f:
            writer.write(f)
        
        chunks_created += 1
        print(f"  Created: {part_path.name} (pages {i+1}-{min(i+n, total_pages)})")
    
    print(f"✅ Split into {chunks_created} chunks")
    return chunks_created
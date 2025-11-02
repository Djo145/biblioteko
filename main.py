#!/usr/bin/env python3
"""
Main orchestrator for converting scanned PDF books to corrected Markdown
"""

import sys
from pathlib import Path
from pdf_utils.markdown_converter import convert_all_parts_to_markdown, save_final_markdown
from pdf_utils.pdf_page_splitter import process_all_pdfs_in_folder
from pdf_utils.pdf_file_splitter import split_pdf
from pdf_utils.pdf_cleaner_and_enhancer import clean_all_parts

def main():
    print("Length of arguments: ",len(sys.argv))

    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_pdf>") 
        sys.exit(1)

    print("Argument 1: ",sys.argv[0])
    print("Argument 2: ",sys.argv[1])
    
    input_pdf = Path(sys.argv[1]) 

    if not input_pdf.exists():
        print(f"Error: PDF file not found: {input_pdf}")
        sys.exit(1)
    
    print("SCANNED BOOK TO MARKDOWN CONVERTER")
    print("=" * 50)
    
    try:
        # Step 1: Split PDF into chunks - and store to raw_parts
        print("\n1. SPLITTING PDF...")
        chunks_created = split_pdf(input_pdf)
        
        # Step 2: Clean the pages (enhance and crop) - and store to cleaned_parts
        print("\n2. CLEANING AND ENHANCING PAGES...")
        pages_cleaned = clean_all_parts()
        
        # # Step 3: Split double pages into single pages - and store to formatted_parts
        # print("\n3. SPLITTING DOUBLE PAGES...")
        # pages_split = process_all_pdfs_in_folder()       

        # Step 3: AI conversion with correction - reads from cleaned_parts (by default) and stores to markdown_output
        print("\n3. AI CONVERSION AND CORRECTION...")
        final_markdown = convert_all_parts_to_markdown()
        
        # Step 4: Save final output
        print("\n4. SAVING FINAL OUTPUT...")
        output_file = save_final_markdown(final_markdown)
        
        # Summary
        print("\n🎉 CONVERSION COMPLETE!")
        print("=" * 50)
        print(f"📖 Original PDF: {input_pdf.name}")
        print(f"📂 Chunks created: {chunks_created}")
        print(f"🧹 Pages cleaned: {pages_cleaned}")
        print(f"💾 Final output: {output_file}")
        print(f"📝 Markdown size: {len(final_markdown)} characters")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
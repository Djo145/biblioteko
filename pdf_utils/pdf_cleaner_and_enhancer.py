import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
from pathlib import Path

from config import CLEANED_PARTS_DIR, RAW_PARTS_DIR

def enhance_image_for_ocr(pil_img):
    """
    Enhance image quality for better OCR results
    """
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.8)
    
    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(pil_img)
    pil_img = enhancer.enhance(2.0)
    
    # Increase brightness
    enhancer = ImageEnhance.Brightness(pil_img)
    pil_img = enhancer.enhance(1.1)
    
    return pil_img

def smart_crop_content(pil_img):
    """
    Crop to content area while preserving reasonable margins
    """
    gray = pil_img.convert('L')
    
    # Enhance contrast for better content detection
    enhancer = ImageEnhance.Contrast(gray)
    gray_enhanced = enhancer.enhance(3.0)
    
    # Invert image (make content white on black background)
    inverted = ImageOps.invert(gray_enhanced)
    
    # Get bounding box of content
    bbox = inverted.getbbox()
    
    if bbox:
        # Add generous margins
        margin_x = int(pil_img.width * 0.05)
        margin_y = int(pil_img.height * 0.08)
        
        x_min = max(0, bbox[0] - margin_x)
        y_min = max(0, bbox[1] - margin_y)
        x_max = min(pil_img.width, bbox[2] + margin_x)
        y_max = min(pil_img.height, bbox[3] + margin_y)
        
        cropped = pil_img.crop((x_min, y_min, x_max, y_max))
        print(f"    ✂️ Cropped to: {cropped.size}")
        return cropped
    
    return pil_img

def clean_pdf_pages(input_pdf_path, output_pdf_path, dpi=300):
    """
    Clean all pages in a PDF: enhance and crop only
    """
    print(f"🧹 Cleaning PDF: {input_pdf_path.name}...")
    
    doc = fitz.open(input_pdf_path)
    cleaned_images = []
    
    for page_num, page in enumerate(doc, 1):
        try:
            # Get high-resolution page image
            pix = page.get_pixmap(dpi=dpi)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            print(f"  Processing page {page_num}: {img.size}")
            
            # Enhance the image
            enhanced_img = enhance_image_for_ocr(img)
            
            # Smart crop to content
            cleaned_img = smart_crop_content(enhanced_img)
            
            cleaned_images.append(cleaned_img)
            print(f"  ✅ Cleaned page {page_num}")
            
        except Exception as e:
            print(f"  ❌ Error cleaning page {page_num}: {e}")
            cleaned_images.append(img)
    
    # Save cleaned pages as new PDF
    if cleaned_images:
        cleaned_images[0].save(
            output_pdf_path,
            save_all=True,
            append_images=cleaned_images[1:],
            quality=95,
            dpi=(dpi, dpi)
        )
    
    doc.close()
    print(f"✅ Cleaned PDF saved: {output_pdf_path}")
    return len(cleaned_images)

def clean_all_parts(input_dir=RAW_PARTS_DIR, output_dir=CLEANED_PARTS_DIR, dpi=300):
    """
    Clean all PDF parts in the input directory
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    cleaned_count = 0
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {input_dir}")
        return 0
    
    for pdf_file in sorted(pdf_files, key=lambda x: x.name):
        print(f"\n{'='*50}")
        output_file = output_path / pdf_file.name
        page_count = clean_pdf_pages(pdf_file, output_file, dpi)
        cleaned_count += page_count
    
    print(f"\n🎉 Total pages cleaned: {cleaned_count}")
    return cleaned_count
from PIL import Image
import fitz  # PyMuPDF
import os
from pathlib import Path
import numpy as np

from config import CLEANED_PARTS_DIR, FORMATTED_PARTS_DIR

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from transformers import AutoImageProcessor, AutoModelForObjectDetection
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not installed. Install with: pip install transformers torch")

# Global model cache
_model = None
_processor = None

def load_document_detection_model():
    """Load the document detection model (cached)."""
    global _model, _processor
    
    if _model is None:
        print("Loading document detection AI model (first time only)...")
        _processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        _model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
        print("Model loaded successfully!")
    
    return _model, _processor


def detect_book_corners_ai(img):
    """
    Detect book page boundaries using AI model.
    
    Args:
        img: PIL Image
    
    Returns:
        Bounding box (left, top, right, bottom)
    """
    try:
        model, processor = load_document_detection_model()
        
        # Prepare image for model
        inputs = processor(images=img, return_tensors="pt")
        
        # Run inference
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Convert outputs to bounding boxes
        target_sizes = torch.tensor([img.size[::-1]])  # (height, width)
        results = processor.post_process_object_detection(
            outputs, threshold=0.5, target_sizes=target_sizes
        )[0]
        
        if len(results["boxes"]) == 0:
            # No detection, return full image
            return (0, 0, img.width, img.height)
        
        # Get the largest detected box
        boxes = results["boxes"].cpu().numpy()
        areas = [(box[2] - box[0]) * (box[3] - box[1]) for box in boxes]
        largest_box = boxes[np.argmax(areas)]
        
        # Convert from [x_min, y_min, x_max, y_max] format
        x1, y1, x2, y2 = map(int, largest_box)
        
        # Add small margin
        margin = 10
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(img.width, x2 + margin)
        y2 = min(img.height, y2 + margin)
        
        return (x1, y1, x2, y2)
        
    except Exception as e:
        print(f"AI detection failed: {e}, falling back to OpenCV")
        return detect_book_corners_opencv(img) if OPENCV_AVAILABLE else detect_book_corners_fallback(img)


def detect_book_corners_opencv(img):
    """
    Detect book page boundaries using Canny edge detection.
    
    Args:
        img: PIL Image
    
    Returns:
        Bounding box (left, top, right, bottom)
    """
    # Convert PIL to OpenCV format
    img_array = np.array(img)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply strong Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 30, 100)
    
    # Dilate edges to connect them
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    
    # Find contours on the dilated edges
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return (0, 0, img.width, img.height)
    
    # Filter contours by area - only keep large ones (likely the book pages)
    min_area = (img.width * img.height) * 0.1  # At least 10% of image
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
    
    if not valid_contours:
        # If no large contours, use the largest one we found
        valid_contours = [max(contours, key=cv2.contourArea)]
    
    # Get bounding box that encompasses all valid contours
    all_points = np.vstack(valid_contours)
    x, y, w, h = cv2.boundingRect(all_points)
    
    # Crop more aggressively - remove outer 2% of detected area
    crop_margin = 0.02
    x_margin = int(w * crop_margin)
    y_margin = int(h * crop_margin)
    
    x = x + x_margin
    y = y + y_margin
    w = w - (2 * x_margin)
    h = h - (2 * y_margin)
    
    return (x, y, x + w, y + h)


def detect_book_corners_fallback(img):
    """
    Fallback edge detection without OpenCV or AI.
    
    Args:
        img: PIL Image
    
    Returns:
        Bounding box (left, top, right, bottom)
    """
    gray = img.convert('L')
    img_array = np.array(gray)
    
    height, width = img_array.shape
    threshold = 235
    edge_threshold = 0.15
    
    # Find edges by scanning
    left = 0
    for x in range(width):
        if np.sum(img_array[:, x] < threshold) > height * edge_threshold:
            left = x
            break
    
    right = width - 1
    for x in range(width - 1, -1, -1):
        if np.sum(img_array[:, x] < threshold) > height * edge_threshold:
            right = x + 1
            break
    
    top = 0
    for y in range(height):
        if np.sum(img_array[y, left:right] < threshold) > (right - left) * edge_threshold:
            top = y
            break
    
    bottom = height - 1
    for y in range(height - 1, -1, -1):
        if np.sum(img_array[y, left:right] < threshold) > (right - left) * edge_threshold:
            bottom = y + 1
            break
    
    return (left, top, right, bottom)


def detect_book_corners(img):
    """
    Detect book page boundaries. Priority: AI > OpenCV > Fallback.
    
    Args:
        img: PIL Image
    
    Returns:
        Bounding box (left, top, right, bottom)
    """
    if TRANSFORMERS_AVAILABLE:
        return detect_book_corners_ai(img)
    elif OPENCV_AVAILABLE:
        return detect_book_corners_opencv(img)
    else:
        return detect_book_corners_fallback(img)


def split_and_rotate_pdf(input_pdf, output_pdf):
    """
    Process PDF: rotate so text is readable left-to-right, detect book corners, 
    crop, and split into left/right pages.
    
    Args:
        input_pdf: Path to input PDF file
        output_pdf: Path to output PDF file with individual pages
    """
    # Open the input PDF
    pdf_document = fitz.open(input_pdf)
    
    # Create new PDF document for output
    output_doc = fitz.open()
    
    # Process each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get page as image with high quality
        mat = fitz.Matrix(3, 3)  # 3x zoom for better quality
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Step 1: Rotate image so text reads left-to-right (not top-to-bottom)
        # If the image is currently in portrait with text sideways, rotate it to landscape
        width, height = img.size
        
        if height > width:
            # Portrait orientation - likely text is sideways, rotate to landscape
            # Rotate 90° clockwise (-90) to make text readable
            img = img.rotate(-90, expand=True)
        
        # Step 2: Detect and crop to book corners (remove background)
        bbox = detect_book_corners(img)
        img_cropped = img.crop(bbox)
        
        # Step 3: Split exactly in half - left page and right page
        cropped_width, cropped_height = img_cropped.size
        mid_point = cropped_width // 2
        
        # Left half = Page 1
        left_page = img_cropped.crop((0, 0, mid_point, cropped_height))
        
        # Right half = Page 2
        right_page = img_cropped.crop((mid_point, 0, cropped_width, cropped_height))
        
        # Add left page to output PDF
        left_pdf_page = output_doc.new_page(
            width=left_page.width,
            height=left_page.height
        )
        left_pdf_page.insert_image(
            left_pdf_page.rect,
            stream=left_page.tobytes("jpeg", "RGB")
        )
        
        # Add right page to output PDF
        right_pdf_page = output_doc.new_page(
            width=right_page.width,
            height=right_page.height
        )
        right_pdf_page.insert_image(
            right_pdf_page.rect,
            stream=right_page.tobytes("jpeg", "RGB")
        )
    
    # Save the output PDF
    output_doc.save(output_pdf)
    output_doc.close()
    pdf_document.close()


def process_all_pdfs_in_folder(input_folder=CLEANED_PARTS_DIR, output_folder=FORMATTED_PARTS_DIR):
    """
    Process all PDF files: rotate to readable orientation, detect book corners,
    crop, and split into individual pages.
    
    Args:
        input_folder: Folder containing PDF files (default: "cleaned_parts")
        output_folder: Folder to save individual page PDFs (default: "formatted_parts")
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all PDF files in input folder
    input_path = Path(input_folder)
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {input_folder}")
        return 0
    
    print(f"Found {len(pdf_files)} PDF file(s) to process\n")
    
    # Process each PDF file
    total_pages = 0
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        
        # Create output file path with same name
        output_file = os.path.join(output_folder, pdf_file.name)
        
        try:
            split_and_rotate_pdf(str(pdf_file), output_file)
            
            # Count pages in output
            output_doc = fitz.open(output_file)
            pages_in_file = len(output_doc)
            output_doc.close()
            total_pages += pages_in_file
            
            print(f"✓ Saved {pages_in_file} pages to: {output_file}\n")
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}\n")
    
    print(f"Complete! Processed {len(pdf_files)} file(s), {total_pages} total pages")
    return total_pages


# Run the program
if __name__ == "__main__":
    input_folder = "cleaned_parts"
    output_folder = "formatted_parts"
    
    process_all_pdfs_in_folder(input_folder, output_folder)
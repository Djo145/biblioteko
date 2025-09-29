import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io
import img2pdf
from pathlib import Path

input_pdf = "./raw_parts/part_1.pdf"
output_pdf = "clean_scan.pdf"

images_pages = []

# Ouvre le PDF
doc = fitz.open(input_pdf)

def auto_orient_and_crop(pil_img):
    """
    Détecte l'orientation et les zones de contenu, puis retourne l'image redressée et cropée.
    """
    # Convert PIL -> OpenCV
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    # Convertir en gris
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    
    # Seuil inversé pour que le contenu soit blanc et fond noir
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Détection des contours externes
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Si aucun contour trouvé, retourner l'image originale
    if not contours:
        return pil_img

    # Combiner tous les contours pour trouver le bounding rect global
    x_min = min([cv2.boundingRect(c)[0] for c in contours])
    y_min = min([cv2.boundingRect(c)[1] for c in contours])
    x_max = max([cv2.boundingRect(c)[0] + cv2.boundingRect(c)[2] for c in contours])
    y_max = max([cv2.boundingRect(c)[1] + cv2.boundingRect(c)[3] for c in contours])
    
    crop_img = pil_img.crop((x_min, y_min, x_max, y_max))
    
    # Détection simple d'orientation : si largeur > hauteur → rotation
    if crop_img.width > crop_img.height:
        crop_img = crop_img.rotate(90, expand=True)
    
    return crop_img

# Parcours toutes les pages
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    
    # Détecte orientation et crop automatique
    cleaned_img = auto_orient_and_crop(img)
    
    images_pages.append(cleaned_img)

# Enregistrer le PDF final
if images_pages:
    images_pages[0].save(
        output_pdf,
        save_all=True,
        append_images=images_pages[1:],
        quality=95
    )

print(f"PDF clean généré : {output_pdf}")

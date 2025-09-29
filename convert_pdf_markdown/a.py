import os
from pathlib import Path
import PyPDF2
import google.generativeai as genai

# --- Charger l'API key ---
with open("./apikey", "r") as fichier:
    apikey = fichier.read().strip()

# --- Configurer Gemini ---
genai.configure(api_key=apikey)
model = genai.GenerativeModel("gemini-2.5-flash")  # ou "gemini-1.5-flash"

# --- Fonction pour découper un PDF en parties ---
def split_pdf(input_path, n=10, output_dir="parts"):
    os.makedirs(output_dir, exist_ok=True)
    reader = PyPDF2.PdfReader(input_path)
    for i in range(0, len(reader.pages), n):
        writer = PyPDF2.PdfWriter()
        for page in reader.pages[i:i+n]:
            writer.add_page(page)
        part_path = os.path.join(output_dir, f"part_{i//n+1}.pdf")
        with open(part_path, "wb") as f:
            writer.write(f)

# --- Découper le PDF source ---
split_pdf('../exemples/copyrighted/cleaned_scan/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf')

# --- Convertir chaque partie en Markdown via Gemini ---
parts_dir = Path("parts")
for file in sorted(parts_dir.iterdir(), key=lambda f: int(''.join(filter(str.isdigit, f.stem)))): 
    if file.is_file():
        print("Converting file:", file.name)
        # Upload du PDF pour Gemini
        uploaded = genai.upload_file(file)
        # Génération du contenu
        prompt = "Convertis ce document en texte markdown stp"
        response = model.generate_content([prompt, uploaded])
        print(response.text)
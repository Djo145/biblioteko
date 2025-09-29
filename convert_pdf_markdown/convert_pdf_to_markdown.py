import os
import pathlib
from pathlib import Path

import PyPDF2
import google.generativeai as genai
from google.generativeai import types


with open("./apikey", "r") as fichier :
    apikey = fichier.read()

filepath = pathlib.Path('../../../Documents/sortie.pdf')

def split_pdf(input_path, n=10, output_dir="parts"):
    os.makedirs(output_dir, exist_ok=True)
    reader = PyPDF2.PdfReader(input_path)
    for i in range(0, len(reader.pages), n):
        writer = PyPDF2.PdfWriter()
        for page in reader.pages[i:i+n] :
            writer.add_page(page)
        part_path = os.path.join(output_dir, f"part_{i//n+1}.pdf")
        with open(part_path, "wb") as f :
            writer.write(f)

split_pdf('../exemples/copyrighted/cleaned_scan/QueSaisJe_1_LesÉtapesDeLaBiologie_1954_7_MauriceCaullery.pdf')

client = genai.Client(api_key=apikey)

for file in sorted(Path("parts").iterdir(), key=lambda f: int(''.join(filter(str.isdigit, f.stem)))) :
    if file.is_file() : 
        print("Conveting file : " + file.name)
        prompt = "Convertit moi ce document en text markdown stp"
        response = client.models.generate_content(
            model = "gemini-2.5-flash", 
            contents = [types.Part.from_bytes(data=file.read_bytes())],
            mime_type ='application/pdf'
        )
        print(response.text)
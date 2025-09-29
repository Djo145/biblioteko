import os
import PyPDF2

def split_pdf(input_path, n=10, output_dir="raw_parts"):
    os.makedirs(output_dir, exist_ok=True)
    reader = PyPDF2.PdfReader(input_path)
    for i in range(0, len(reader.pages), n):
        writer = PyPDF2.PdfWriter()
        for page in reader.pages[i:i+n] :
            writer.add_page(page)
        part_path = os.path.join(output_dir, f"part_{i//n+1}.pdf")
        with open(part_path, "wb") as f :
            writer.write(f)

split_pdf('../exemples/copyrighted/raw_scan/1_HistoireDeLaBiologie_1954_7_MauriceCaullery.pdf')

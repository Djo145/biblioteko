import pathlib 

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
        part_path = os.path.join(output_dir, f"")


import os
from PyPDF2 import PdfMerger

def merge_pdfs(folder_path, output_path):
    # Create a PdfMerger object
    merger = PdfMerger()

    # Loop through all the PDF files in the folder
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, pdf_file)
            merger.append(pdf_path)
            print(f"Added: {pdf_file}")


    # Write the combined PDF to the output path
    with open(output_path, 'wb') as output_pdf:
        merger.write(output_pdf)
        print(f"PDF merged and saved as {output_path}")

# Example usage
# for i in range(1,8):
#     folder_path = f'pictures/Maths/Chap_{i}'
#     output_path = f'PDFs/Maths_chap_{i}.pdf'
#     merge_pdfs(folder_path, output_path)


folder_path = f'PDFs'
output_path = f'PDFs/Maths_full1.pdf'
merge_pdfs(folder_path, output_path)

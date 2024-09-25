

import os
from PyPDF2 import PdfMerger

def merge_pdfs(folder_path, output_path, subject):
    # Create a PdfMerger object
    merger = PdfMerger()

    # Loop through all the PDF files in the folder
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf') and pdf_file.startswith(subject):
            pdf_path = os.path.join(folder_path, pdf_file)
            merger.append(pdf_path)
            print(f"Added: {pdf_file}")


    # Write the combined PDF to the output path
    with open(output_path, 'wb') as output_pdf:
        merger.write(output_pdf)
        print(f"PDF merged and saved as {output_path}")

# Example usage
# for i in range(1,8):
#     folder_path = f'pictures/Chemistry/Chap_{i}'
#     output_path = f'PDFs/Chemistry_chap_{i}.pdf'
#     merge_pdfs(folder_path, output_path)

# hoa
# chap 1 : 70 cau : 1-> 136 
# chap 2 : 50 cau : 137-> 232
# chap 3 : 100 cau : 233 -> 424
# chap 4 : 30 cau : 425 -> 484
# chap 5 : 80 cau : 485 -> 640
# chap 6 : 80 cau : 641 -> 796
# chap 7 : 50 cau : 797 -> 894

subject_d = {
    "L" : "Physics",
    "H" : "Chemistry",
    "T" : "Maths"
}

folder_path = f'PDFs'
output_path = f'PDFs/Chemistry_full2.pdf'
merge_pdfs(folder_path, output_path, subject_d["H"])

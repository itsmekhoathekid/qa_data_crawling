from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_pdf_path, start_page, end_page):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Lấy số trang của file PDF
    num_pages = len(reader.pages)

    # Đảm bảo rằng số trang hợp lệ
    if start_page < 1 or end_page > num_pages or start_page > end_page:
        raise ValueError(f"Số trang không hợp lệ. File PDF chỉ có {num_pages} trang.")

    # Cắt file PDF từ trang bắt đầu đến trang kết thúc
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    # Ghi kết quả vào file PDF mới
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Đường dẫn tới file PDF gốc
input_pdf_path = r'C:\Users\VIET HOANG - VTS\Desktop\crawling\PDFs\Chemistry_full1.pdf'



dic = {
    "H" : {
        1 : (1, 136),
        2 : (137, 232),
        3 : (233, 424),
        4 : (425, 484),
        5 : (485, 640),
        6 : (641, 796),
        7 : (797, 894)
    }
}

for i in dic["H"]:
    start_page, _ = dic["H"][i]
    end_page = start_page + 69
    output_pdf_path = f'PDFs/Chemistry_chap_{i}.pdf'
    split_pdf(input_pdf_path, output_pdf_path, start_page, end_page)

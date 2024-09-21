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
input_pdf_path = r'PDFs\Maths_chap_1.pdf'
# Đường dẫn tới file PDF kết quả sau khi cắt
output_pdf_path = r'PDFs\Maths_chap_1_part1.pdf'
# Số trang bắt đầu và kết thúc (đánh số trang từ 1)
start_page = 1
end_page = 300

# Gọi hàm cắt file PDF
split_pdf(input_pdf_path, output_pdf_path, start_page, end_page)
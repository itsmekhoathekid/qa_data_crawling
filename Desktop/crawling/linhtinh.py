import os
from PIL import Image  # pip install pillow

output_dir = './PDFs'
source_dir = './pictures/Math/chap_1'

# Kiểm tra nếu thư mục lưu PDF không tồn tại thì tạo mới
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Hàm để cắt và chuyển ảnh thành PDF
def crop_and_convert_image_to_pdf(source_image_path, output_pdf_path):
    # Mở ảnh gốc
    image = Image.open(source_image_path)
    x2, y2 = image.size
    crop_box = (0,0,x2,y2)
    # Cắt ảnh theo tọa độ crop_box (x1, y1, x2, y2)
    cropped_image = image.crop(crop_box)

    # Chuyển đổi ảnh sang RGB (bắt buộc cho PDF)
    cropped_image_rgb = cropped_image.convert('RGB')

    # Lưu ảnh đã cắt dưới dạng PDF
    cropped_image_rgb.save(output_pdf_path)

# Duyệt qua tất cả các file trong thư mục source_dir
for file in os.listdir(source_dir):
    if file.split('.')[-1].lower() in ('png', 'jpg', 'jpeg'):
        # Đường dẫn file ảnh gốc
        source_image_path = os.path.join(source_dir, file)

        # Đường dẫn file PDF đầu ra
        output_pdf_path = os.path.join(output_dir, f'{file.split(".")[-2]}.pdf')


        # Gọi hàm cắt và chuyển đổi ảnh thành PDF
        crop_and_convert_image_to_pdf(source_image_path, output_pdf_path)

        print(f'Đã cắt và lưu file PDF: {output_pdf_path}')
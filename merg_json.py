import json

# Đọc nội dung của file đầu tiên chứa câu hỏi
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Đọc file thứ hai, xử lý nếu cần
def read_custom_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Nối hai file lại với nhau
def merge_json_files(questions_data, image_data):
    merged_data = []
    for question in questions_data:
        # Tìm đối tượng tương ứng trong image_data
        for image in image_data:
            if question["id"] == image["id"] and image["answer"] != None:
                question["image_source"] = image["image_source"]
                question["answer"] = image["answer"]
                question["difficulty"] = image["difficulty"]
        merged_data.append(question)
    return merged_data

# Ghi kết quả ra file JSON mới
def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


images_file_path = r"C:\Users\VIET HOANG - VTS\Downloads\fixed_image_structure_demo.json"
questions_file_path = 'json_full/merged_physics.json'
output_file_path = 'json_full/merged_physics.json'

# Đọc dữ liệu từ hai file
questions_data = read_json_file(questions_file_path)
images_data = read_custom_json_file(images_file_path)

# Nối dữ liệu từ hai file
merged_data = merge_json_files(questions_data, images_data)

# Ghi kết quả ra file mới
write_json_file(output_file_path, merged_data)
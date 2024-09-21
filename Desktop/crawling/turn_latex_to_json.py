import json
import re

def extract_questions_from_latex(latex, subject_id):
    # Tìm tất cả các block câu hỏi và lời giải (tìm theo ID câu hỏi và chia khối)
    blocks = re.split(rf"(\\section\*\{{{subject_id}\d+\}})", latex)  # Tìm tất cả các phần ID câu hỏi
    
    questions_data = []
    
    for i in range(1, len(blocks), 2):  # Lặp qua các cặp (ID và nội dung)
        question_id_block = blocks[i]
        block = blocks[i + 1]

        # Trích xuất ID câu hỏi (ID đi kèm với \section*{subject_id...})
        id_match = re.search(rf"\\section\*\{{({subject_id}\d+)\}}", question_id_block)
        question_id = id_match.group(1) if id_match else None

        # Trích xuất và xử lý câu hỏi
        questions_data.extend(process_question_block(question_id, block))
    
    return questions_data

def clean(block):
    block_cleaned = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", "", block, flags=re.DOTALL)  # Loại bỏ bảng
    block_cleaned = re.sub(r"\\includegraphics\[.*?\]\{.*?\}", "", block_cleaned, flags=re.DOTALL)  # Loại bỏ hình ảnh
    block_cleaned = re.sub(r"\\begin\{center\}.*?\\end\{center\}", "", block_cleaned, flags=re.DOTALL)  # Loại bỏ phần center
    return block_cleaned

def process_question_block(question_id, block):
    # Loại bỏ các phần bảng biểu hoặc hình ảnh trong block, nhưng giữ lại câu hỏi
    block_cleaned = clean(block)

    # Trích xuất câu hỏi chính (loại bỏ tất cả các lựa chọn)
    question_match = re.search(r"\\section\*\{Câu \d+\}(.*?)\\section\*\{Lời giải.*?\}", block_cleaned, re.DOTALL)
    question = question_match.group(1).strip() if question_match else None

    # Nếu không tìm thấy câu hỏi, bỏ qua
    if not question:
        print(f"Không tìm thấy câu hỏi cho ID: {question_id}")
        return []

    # Trích xuất các lựa chọn (A, B, C, D), xử lý nhiều dòng
    options = re.findall(r"([A-D])\.\s*(.*?)\s*(?=\\\\|\Z)", block_cleaned, re.DOTALL)

    # Trích xuất lời giải
    explanation_match = re.search(r"\\section\*\{Lời giải.*?\}(.*?)(?=(Đáp án cần chọn là|\\section\*\{{subject_id}\d+\}))", block_cleaned, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None
    explanation = clean(str(explanation))

    # Tạo đối tượng JSON
    question_data = {
        "id": question_id,
        "question": question,  # Chỉ chứa phần câu hỏi
        "options": [f"{opt[0]}. {opt[1]}" for opt in options],
        "explain": explanation
    }

    if question_data["question"] is None:
        print(f'{question_data["id"]} : ko có câu hỏi')
    if question_data["options"] is None:
        print(f'{question_data["id"]} : ko có A, B, C, D')
    if question_data["explain"] is None:
        print(f'{question_data["id"]} : ko có explain')

    return [question_data]

# Đọc file LaTeX
path_h = r"C:\Users\VIET HOANG - VTS\Downloads\merged_output3\2024_09_18_984ace34b4147d649006g\2024_09_18_984ace34b4147d649006g.tex"
path_f = "test.tex"
path_t = r"C:\Users\VIET HOANG - VTS\Downloads\Maths_full1\2024_09_20_c74e9393375aab4b22f9g\2024_09_20_c74e9393375aab4b22f9g.tex"

with open(path_f, 'r', encoding='utf-8') as file:
    latex_text = file.read()

# Chuyển đổi LaTeX thành danh sách JSON format với subject_id là "H"
questions_json = extract_questions_from_latex(latex_text, 'T')

# Chuyển đổi kết quả thành JSON (giữ nguyên LaTeX trong chuỗi)
json_output = json.dumps(questions_json, ensure_ascii=False, indent=4)
# json_output = json_output.replace("\\\\", '\\')
print(json_output)
# output_path = "maths.json"

# # Lưu nội dung json_output vào tệp JSON
# with open(output_path, 'w', encoding='utf-8') as json_file:
#     json_file.write(json_output)
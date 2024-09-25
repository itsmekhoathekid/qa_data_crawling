import json
import re
def add_answer_before_section(block_cleaned, answer="D"):
    # Define a regex pattern to match each \section*{L####}
    section_pattern = r"(\\section\*\{L\d+\})"
    
    # Define the replacement that adds the answer before each section
    replacement = f"Đáp án cần chọn là: {answer}\n\\1"
    
    # Perform the substitution to insert the answer before each section
    modified_block = re.sub(section_pattern, replacement, block_cleaned)
    
    return modified_block

def clean_latex(latex):
    # Sử dụng biểu thức chính quy để loại bỏ các section liên quan đến các mức độ câu hỏi
    block_cleaned = re.sub(r"\\section\*\{\s*Vận dụng\s*\}", "", latex, flags=re.DOTALL)
    block_cleaned = re.sub(r"\\section\*\{\s*Thông hiểu\s*\}", "", block_cleaned, flags=re.DOTALL)
    block_cleaned = re.sub(r"\\section\*\{\s*Nhận biết\s*\}", "", block_cleaned, flags=re.DOTALL)
    block_cleaned = re.sub(r"\\section\*\{\s*Vận dụng cao\s*\}", "", block_cleaned, flags=re.DOTALL)
    return block_cleaned
def extract_questions_from_latex(latex, subject_id):
    # Tìm tất cả các block câu hỏi và lời giải (tìm theo ID câu hỏi và chia khối)

    latex = clean_latex(latex)
    latex = add_answer_before_section(latex)

    blocks = re.split(rf"(\\section\*\{{{subject_id}\d+\}})", latex)  # Tìm tất cả các phần ID câu hỏi
    
    questions_data = []
    
    # Xử lý trường hợp nếu đoạn đầu tiên của tài liệu không bắt đầu bằng \section*{subject_id...}
    # if not latex.startswith(f"\\section*{{{subject_id}}}"):
    #     # Nếu không có \section*{subject_id...} ở đầu tài liệu, lấy nội dung trước phần đầu tiên của \section*{subject_id...}
    #     pre_block = re.split(rf"(\\section\*\{{{subject_id}\d+\}})", latex, maxsplit=1)
    #     if len(pre_block) > 1:
    #         # Lấy phần câu hỏi trước \section*{subject_id...} đầu tiên
    #         questions_data.extend(process_question_block(f"{subject_id}0101001", pre_block[0]))  # ID giả định cho câu hỏi đầu

    for i in range(1, len(blocks), 2):  # Lặp qua các cặp (ID và nội dung)
        question_id_block = blocks[i]
        block = blocks[i + 1]

        # Trích xuất ID câu hỏi (ID đi kèm với \section*{subject_id...})
        id_match = re.search(rf"\\section\*\{{({subject_id}\d+)\}}", question_id_block)
        question_id = id_match.group(1) if id_match else None

        # Trích xuất và xử lý câu hỏi
        questions_data.extend(process_question_block(question_id, block,subject_id))
    
    return questions_data

def clean(block):
    block_cleaned = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", "", block, flags=re.DOTALL)  # Loại bỏ bảng
    block_cleaned = re.sub(r"\\includegraphics\[.*?\]\{.*?\}", "", block_cleaned, flags=re.DOTALL)  # Loại bỏ hình ảnh
    block_cleaned = re.sub(r"\\begin\{center\}.*?\\end\{center\}", "", block_cleaned, flags=re.DOTALL)  # Loại bỏ phần center

    return block_cleaned

def clean_options(block):
     # Loại bỏ phần "Lời giải của GV Loigiaihay.com" và "Đáp án cần chọn là"
    block_cleaned = re.sub(r"\\section\*\{Lời giải của GV Loigiaihay\.com\}", "", block, flags=re.DOTALL)
    block_cleaned = re.sub(r"Đáp án cần chọn là:.*", "", block_cleaned, flags=re.DOTALL)

    # Remove any other LaTeX sections that might interfere
    block_cleaned = re.sub(r"\\section\*{.*?}", "", block_cleaned, flags=re.DOTALL)
    return block_cleaned



def process_question_block(question_id, block,subject_id):
    # Loại bỏ các phần bảng biểu hoặc hình ảnh trong block, nhưng giữ lại câu hỏi

    block_cleaned = clean(block)

    # Trích xuất câu hỏi chính (loại bỏ tất cả các lựa chọn)
    pattern = r"Lời giải của GV \\href{.*}{(.*)}\\\\"
    replacement = r"\\section*{Lời giải của GV \1}"
    block_cleaned = re.sub(pattern, replacement, block_cleaned, flags=re.DOTALL)



    question_match = re.search(r"Câu \d+\s*(.*?)\s*(?=[A-D]\.\s)", block_cleaned, re.DOTALL)
    if question_match is None:
        question_match = re.search(r"\\section\*\{Câu \d+\}\s*(.*?)\s*(?=[A-D]\.\s)", block_cleaned, re.DOTALL)
    
    question = question_match.group(1).strip() if question_match else None

    options_pattern = r"(A\..*?)(B\..*?)(C\..*?)(D\..*)"
    options = re.findall(options_pattern, block_cleaned, re.DOTALL)
    if options == []:
        options_pattern = r"(A\..*?)(D..*?)(B\..*?)(C\..*)"
        options = re.findall(options_pattern, block_cleaned, re.DOTALL)
        if options == []:
            options_pattern = r"(A\..*?)(B..*?)([Cc]\..*?)(D\..*)"
            options = re.findall(options_pattern, block_cleaned, re.DOTALL)
    
    option_list = [clean_options(opt) for opt in options[0]] if options else []
    # Trích xuất lời giải
    explanation_pattern = fr"\\section\*\{{Lời giải.*?\}}(.*?)(?=(Đáp án cần chọn là|\\section\*\{{{subject_id}\d+\}}))"
    explanation_match = re.search(explanation_pattern, block_cleaned, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else None
    explanation = clean(str(explanation)) if explanation else None
    # Tạo đối tượng JSON
    
    if option_list and explanation and explanation in option_list[-1]:
        option_list[-1] = option_list[-1].replace(explanation, "").strip()
    
    
    question_data = {
        "id": question_id,
        "question": question,  # Chỉ chứa phần câu hỏi
        "options": option_list,
        "explain": explanation
    }
    
    if question_data["question"] is None:
        print(f'{question_data["id"]} : ko có câu hỏi')
    if question_data["options"] == []:
        print(f'{question_data["id"]} : ko có A, B, C, D')
    if question_data["explain"] is None:
        print(f'{question_data["id"]} : ko có explain')
    return [question_data]

# Đọc file LaTeX
path_h = r"C:\Users\VIET HOANG - VTS\Downloads\merged_output3\2024_09_18_984ace34b4147d649006g\2024_09_18_984ace34b4147d649006g.tex"
path_f = "test.tex"
path_t = r"C:\Users\VIET HOANG - VTS\Downloads\Maths_full1\2024_09_20_c74e9393375aab4b22f9g\2024_09_20_c74e9393375aab4b22f9g.tex"
path_l = r"C:\Users\VIET HOANG - VTS\Downloads\physics_full\2024_09_22_72c02097c641f684ec5ag\2024_09_22_72c02097c641f684ec5ag.tex"
path_h = r"C:\Users\VIET HOANG - VTS\Downloads\Chemistry_full2\2024_09_24_eec292b3ed50b5dbc12cg\2024_09_24_eec292b3ed50b5dbc12cg.tex"
with open(path_h, 'r', encoding='utf-8') as file:
    latex_text = file.read()

# Chuyển đổi LaTeX thành danh sách JSON format với subject_id là "H"
questions_json = extract_questions_from_latex(latex_text, 'H')

# Chuyển đổi kết quả thành JSON (giữ nguyên LaTeX trong chuỗi)
json_output = json.dumps(questions_json, ensure_ascii=False, indent=4)
# json_output = json_output.replace("\\\\", '\\')
# print(json_output)
output_path = "json_qa/Chemistry.json"

# Lưu nội dung json_output vào tệp JSON
with open(output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)
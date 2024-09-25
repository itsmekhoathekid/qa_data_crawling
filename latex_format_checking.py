import json
import openai
import os

# Thiết lập API key OpenAI
openai.api_key = ""  # Thay bằng API key của bạn

def PromptOptions(json_file):
    options = json_file['options']
    explanation = json_file['explain']
    id = json_file['question']
    
    prompt = f"""Hãy kiểm tra xem các đáp án trong nội dung sau có đúng với định dạng latex cho các công thức hóa hay không. Nếu định dạng công thức hóa học latex ở đáp án là sai, hãy sửa lại nó cho đúng (đừng có thiếu $ trong công thức). 
    Nếu có số thập phân thì lấy dấu ',' chứ không phải dấu '.'.
    Đừng thêm dấu " trong nội dung options.
    Xóa hết các dấu gạch ngang / không cần thiết
    Không cần ghi gì hết, chỉ ghi đúng theo format : A. nội dung câu a__B.nội dung câu b__C. nội dung câu c__D. nội dung câu D.
    Hãy giữ nguyên thứ tự các đáp án A, B, C, D. Nếu câu D nào mà có dính phần explain thì xóa phần explain của câu D đi.
    Sau đây là phần options : {options}, và đây là phần explain : {explanation}
    """
    
    return prompt

def promptQuesiton(json_file):
    question = json_file['question']
    prompt = f"""format lại question sau cho chuẩn định dạng latex, loại bỏ các từ không liên quan như : Nhận biết, Vận dụng, Thông hiểu, Vận dụng cao , và các phần dư thừa như section, text ... {question}, 
            Ghi lại theo format sau : nội dung câu hỏi . 
            Lưu ý output chỉ ghi lại câu hỏi theo format.
        """
    return prompt
# Hãy trả lời y chang với format của file json ban đầu, không cần ghi gì thêm, chỉ sửa những đoạn sai, những đoạn không sai thì giữ nguyên. 
# Không cần nhận xét gì hết chỉ cần ghi "Có chỉnh sửa" cho những câu cần chỉnh sửa và ghi format của json sau khi có những thay đổi (hoặc không).
# Hãy load cái phần options từ string qua list
def call_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Thay thế bằng tên mô hình chính xác của bạn, ví dụ 'gpt-4'
        messages=[
            {"role": "system", "content": "Bạn là một chuyên gia về LaTeX và môn Hóa, có khả năng kiểm tra và đánh giá định dạng LaTeX. Bạn cần kiểm tra xem định dạng LaTeX của các câu hỏi và đáp án trong tài liệu này có đúng không và sửa chúng nếu cần thiết."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Bạn có thể tùy chỉnh giá trị này
        max_tokens=1000,  # Điều chỉnh số lượng token trả về theo nhu cầu
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']

# L0407033
# L0105022
# L0405023
# L0106029
# L0106026
# L0205023
# L0306026

# L0304020


path = 'json_full/merged_physics.json'
# Đọc file JSON
with open(path, 'r', encoding='utf-8') as file:
    data = json.load(file)

def process(data):
    return data.split("__")

dic = {
    "L0101002" : {
        "options" : [
            "A. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = k2\\pi$",
            "B. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = (2k + 1)\\pi$",
            "C. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = \\frac{2k+1}{2}\\pi$",
            "D. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = \\alpha$ bất kỳ"
        ]
    },
    "L0101001" : {
        "options" : [
            "A. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = k2\\pi$",
            "B. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = (2k + 1)\\pi$",
            "C. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = \\frac{2k+1}{2}\\pi$",
            "D. $\\Delta \\varphi = \\varphi_{2} - \\varphi_{1} = \\alpha$ bất kỳ"
        ]
    },
    "L0101003" : {
        "options" : [
            "A. $2k\\pi$ với $k = 0, \\pm1, \\pm2, \\ldots$",
            "B. $(2k + 0,5)\\pi$ với $k = 0, \\pm1, \\pm2, \\ldots$",
            "C. $(k + 0,5)\\pi$ với $k = 0, \\pm1, \\pm2, \\ldots$",
            "D. $(2k + 1)\\pi$ với $k = 0, \\pm1, \\pm2, \\ldots$"
        ]
    },
    "L0702010" : {
        "options" : [
            "A. $\\Delta m = Zm_n + (A - Z)m_p - m_X$",
            "B. $\\Delta m = Zm_p + (A - Z)m_n - m_X$",
            "C. $\\Delta m = m_X - Zm_p + (A - Z)m_n$",
            "D. $\\Delta m = Zm_p + (A - Z)m_n + m_X$"
        ]
    },"L0407033": {
        "options": [
            "A. $\\lambda_{max} = c \\frac{\\sqrt{LC_{max}}}{2\\pi}$",
            "B. $\\lambda_{max} = 2\\pi c \\sqrt{\\frac{L}{C_{min}}}$",
            "C. $\\lambda_{max} = \\frac{2\\pi c}{\\sqrt{LC_{min}}}$",
            "D. $\\lambda_{max} = 2\\pi c \\sqrt{\\frac{L}{C_{max}}}$"
        ]
    },
    "L0105022": {
        "options": [
            "A. $A = 8cm; T = 0,56s$",
            "B. $A = 6cm; T = 0,28s$",
            "C. $A = 6cm; T = 0,56s$",
            "D. $A = 4cm; T = 0,28s$"
        ]
    },
    "L0405023": {
        "options": [
            "A. $q = 5 x 10^{-10} \\cos(10^7 t + \\frac{\\pi}{2}) C$",
            "B. $q = 2, 5 x 10^{-10} \\sin(10^7 t) C$",
            "C. $q = 5 x 10^{-9} \\cos(2.10^7 t + \\frac{\\pi}{2}) C$",
            "D. $q = 2,5 x 10^{-9} \\cos(2.10^7 t) C$"
        ]
    },
    "L0106029": {
        "options": [
            "A. $0$",
            "B. $\\frac{\\pi}{2}$",
            "C. $\\pi$",
            "D. $-\\frac{\\pi}{2}$"
        ]
    },
    "L0106026": {
        "options": [
            "A. $4cm$",
            "B. $\\pm 4cm$",
            "C. $16cm$",
            "D. $2cm$"
        ]
    },
    "L0205023": {
        "options": [
            "A. $16Hz$ đến $2.10^4 Hz$",
            "B. $16Hz$ đến $20MHz$",
            "C. $16Hz$ đến $200KHz$",
            "D. $16Hz$ đến $2KHz$"
        ]
    },
    "L0306026": {
        "options": [
            "A. $i = \\frac{U_0}{\\omega L} \\cos(\\omega t + \\frac{\\pi}{2})$",
            "B. $i = \\frac{U_0 \\omega L}{\\omega L} \\cos(\\omega t + \\frac{\\pi}{2})$",
            "C. $i = \\frac{U_0}{\\omega L} \\cos(\\omega t - \\frac{\\pi}{2})$",
            "D. $i = \\frac{U_0 \\omega L}{\\omega L} \\cos(\\omega t)$"
        ]
    }
}


for item in data:
    # prompt = PromptOptions(item)
    # if item["id"] not in dic.keys():
    #     result = call_gpt(prompt)
    #     result = process(result)
    # else:
    #     result = dic[item["id"]]["options"]
    # item["options"] = result
    # # prompt = promptQuesiton(item)
    # # result = call_gpt(prompt)
    # # item["question"] = result
    # print(f"{result}")

    if item["id"] in dic.keys():
        item["options"] = dic[item["id"]]["options"]
    



# Lưu file JSON sau khi đã kiểm tra
with open(path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("xong")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException
import os
import json 
import time
import re
import os
from fpdf import FPDF
from PIL import Image

def Create_webdriver():
    options = webdriver.EdgeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1500,1000")
    options.add_argument("--disable-notifications")

    # Khởi tạo WebDriver cho Microsoft Edge
    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()),
        options=options
    )
    return driver

def Click_start_button(driver):
    try:
        # Tìm nút "Bắt đầu" bằng class
        start_button = driver.find_element(By.CSS_SELECTOR, 'a.text-white.btn-green.btn-action')
        start_button.click()
        print("Đã click vào nút 'Bắt đầu'")
        time.sleep(2)  # Chờ trang tải câu hỏi
    except NoSuchElementException:
        print("Không tìm thấy nút 'Bắt đầu'")

def Select_type_of_question(driver):
    try:
        # Tìm nút "Bắt đầu" bằng class
        _button = driver.find_element(By.CSS_SELECTOR, 'div.icon.iconKingHat')
        _button.click()
        print("Đã click vào nút 'Làm tất cả'")
        time.sleep(2)  # Chờ trang tải câu hỏi
    except NoSuchElementException:
        print("Không tìm thấy nút 'Làm tất cả'")

def Dump_contents_Json(id,question,img_src,difficulty,options,answer,explain,name_file):
    data = {
        "id":id,
        "question": question,
        "image_source":img_src,
        "difficulty":difficulty,
        "options": [options[i] for i in range(len(options))],
        "answer": answer,
        "explain":explain
    }
    file_path = os.path.join(f'D:\Code\Python\projects', name_file)
    with open(file_path, 'a', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def get_question(driver):
    question_text = driver.find_element(By.CSS_SELECTOR, 'div.content-quiz.mg-top-10').text
    question_text_cleaned = re.sub(r'\s+', ' ', question_text).strip()
    print(question_text_cleaned)

    return question_text_cleaned

def get_difficulty(driver):
    # difficulty_text = ''
    # try:
    #     difficulty_text = driver.find_element(By.CSS_SELECTOR,'span.clf.pull-right.bgblue1').text
    #     try: 
    #         difficulty_text = driver.find_element(By.CSS_SELECTOR,'span.clf.pull-right.bglogo2').text
    difficulty_text = driver.find_element(By.CSS_SELECTOR,'div.vn-tit-question span').text

    return difficulty_text

# Crawl Toan
# def get_options(driver):
#     options = []
#     options_elements = driver.find_elements(By.CSS_SELECTOR, 'div.cursor-pointer.mg-bottom-10.col-xs-6.col-md-6.col-sm-4')
                                                                    
#     for element in options_elements:
#         text = element.text
#         option_cleaned = re.sub(r'\s+', ' ', text).strip()
#         options.append(option_cleaned)
#         print(option_cleaned)

#     return options

# Crawl VatLi
def get_options(driver):
    options = []
    css_selectors = [
        'div.cursor-pointer.mg-bottom-10.col-xs-12.col-md-12.col-sm-4',
        'div.cursor-pointer.mg-bottom-10.col-xs-6.col-md-6.col-sm-4',
        'div.cursor-pointer.mg-bottom-10.col-xs-3.col-md-3.col-sm-4'
    ]

    options_elements = None

    for selector in css_selectors:
        try:
            options_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if options_elements:
                break  
        except:
            continue 

    if not options_elements:
        return options  

    for element in options_elements:
        text = element.text
        option_cleaned = re.sub(r'\s+', ' ', text).strip()
        options.append(option_cleaned)
        print(option_cleaned)

    return options

def select_key_and_get_answer_and_explain(driver):
    circle_select = driver.find_element(By.CSS_SELECTOR,'span.arround-select')
    circle_select.click()
    time.sleep(4)
    check_button = driver.find_element(By.CSS_SELECTOR,'a.false.cursor-pointer.text-white.btn-green.btn-action.visible')
    check_button.click()
    time.sleep(4)
    try:
        # status_ans = driver.find_element(By.CSS_SELECTOR,'span.font-roboto-b.font-size-18.color-green').text
        # if status_ans == 'Bạn đã chọn đúng':
            explain_button = driver.find_element(By.CSS_SELECTOR,'a.cursor-pointer.bg-grey.btn-action') 
            explain_button.click()
            time.sleep(3)
            explain_text = driver.find_elements(By.CSS_SELECTOR,'div.solution-item')
            explain_element = explain_text[-1]
    except:
        explain_text = driver.find_elements(By.CSS_SELECTOR,'div.solution-item')
        explain_element = explain_text[-1]
    # take_element_screenshot(driver,explain_element,folder_path,file_name,pdf=pdf)
    # explain_text = explain_text[-1].text
    # explain_text_cleaned = re.sub(r'\s+', ' ', explain_text).strip()
    # print(explain_text_cleaned)
    # key_answer = explain_text_cleaned[-1]
    # print(key_answer)
    return explain_element

def get_url_image(driver):
    try:
        element = driver.find_element(By.CSS_SELECTOR, 'div.content-quiz.mg-top-10 img')
        src = element.get_attribute('src')
        print(src)
        
        return src
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def Click_next_question(driver):
    next_question_button = driver.find_element(By.CSS_SELECTOR,'a.cursor-pointer.text-white.btn-green.btn-action.visible')
    next_question_button.click()
    time.sleep(5)

def get_QAs_element(driver):
    QAs_element = driver.find_element(By.CSS_SELECTOR, 'div.col-sm-11')
    return QAs_element

from PIL import Image
import os

def take_element_screenshot(driver, element, folder_path, pdf_file_name, pdf, id):
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Define the PDF file path
    pdf_file_path = os.path.join(folder_path, pdf_file_name + '.pdf')
    
    # Create a new PDF or load existing PDF
    pdf.add_page()  # Add a page to start the PDF
    
    # Add the ID at the top of the page
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"ID: {id}", ln=True, align='L')  # ID text at the top left of the page
    
    # Capture screenshot of the question element and save it temporarily as a PNG
    screenshot_file_path = os.path.join(folder_path, f'q_{id}.png')
    element.screenshot(screenshot_file_path)
    print(f"Screenshot of element saved temporarily at {screenshot_file_path}")
    
    # # Open the image using PIL and convert to RGB
    # image = Image.open(screenshot_file_path)
    # image = image.convert('RGB')
    
    # # Get image dimensions and convert to millimeters (assuming 96 DPI)
    # img_width, img_height = image.size
    # mm_width = img_width * 0.264583
    # mm_height = img_height * 0.264583

    # # Add the question image below the ID
    # y_position = 20  # Leave some space below the ID
    # pdf.image(screenshot_file_path, 10, y_position, mm_width, mm_height)
    
    # Capture screenshot of the answer element and save it temporarily as a PNG
    element2 = select_key_and_get_answer_and_explain(driver)  # Assuming this function returns a web element
    screenshot_file_path_answer = os.path.join(folder_path, f'a_{id}.png')
    element2.screenshot(screenshot_file_path_answer)
    print(f"Screenshot of answer saved temporarily at {screenshot_file_path_answer}")
    
    # # Open the answer image and convert to RGB
    # image_answer = Image.open(screenshot_file_path_answer)
    # image_answer = image_answer.convert('RGB')

    # # Get image dimensions for the answer
    # img_width_answer, img_height_answer = image_answer.size
    # mm_width_answer = img_width_answer * 0.264583
    # mm_height_answer = img_height_answer * 0.264583

    # # Add the answer image below the question image
    # pdf.image(screenshot_file_path_answer, 10, y_position + mm_height + 10, mm_width_answer, mm_height_answer)  # 10mm padding

    # # Save the updated PDF
    # pdf.output(pdf_file_path)
    # print(f"Screenshot added to PDF file at {pdf_file_path}")
    
    # Optionally, remove the temporary screenshot files
    # os.remove(screenshot_file_path)
    # os.remove(screenshot_file_path_answer)


file_path = 'Link_Maths.json'
with open(file_path, 'r', encoding='utf-8') as file:
    links_physics = json.load(file)

j = 0
for chapter in range(1,8):
    for link in links_physics[str(chapter)]:
            
        driver = Create_webdriver()
        driver.get(link)

        Click_start_button(driver)
        Select_type_of_question(driver)
        
        
        try:
            for i in range(1,10):
                j+=1
                suffix = '{:05}'.format(0 + j)
                prefix = f'T{str(chapter).zfill(2)}'
                id = f"{prefix}{suffix}"
                try:
                    QAs = get_QAs_element(driver)
                    pdf = FPDF()
                    take_element_screenshot(driver, element=QAs, folder_path=f'pictures//Math//chap_{chapter}',
                                            pdf_file_name=f'qa_{id}',pdf=pdf, id = id)
                    question = get_question(driver)
                    difficulty = get_difficulty(driver)
                    options = get_options(driver)
                    src = get_url_image(driver)
                    time.sleep(4)
                    
                    Click_next_question(driver)
                    # Dump_contents_Json(id, question, src, difficulty, options, answer, explain ,'Chemistry_C1.NO1.json')
                
                    print(f"==================Question {i} processed and saved.=====================")
                    break
                except NoSuchElementException as e:
                    try:
                        time.sleep(4)
                        go_head_button = driver.find_element(By.CSS_SELECTOR,'a.cursor-pointer.text-white.bg-green.btn-action')
                        go_head_button.click()
                        time.sleep(4)
                    except:
                        continue
        
                
        finally:
            # print("==============xong==================")
            driver.quit()    



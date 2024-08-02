import fitz
from tqdm import tqdm
import requests
import os
import re
import base64
import argparse

def get_access_token(api_key, secret_key):
    auth_url = 'https://aip.baidubce.com/oauth/2.0/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': secret_key
    }
    response = requests.post(auth_url, data=payload)
    result = response.json()
    return result['access_token']

def ocr_image(image_path, access_token):
    with open(image_path, 'rb') as f:
        img_data = f.read()

    img_base64 = base64.b64encode(img_data).decode('utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'access_token': access_token
    }
    data = {
        'image': img_base64
    }
    response = requests.post(BAIDU_OCR_URL, headers=headers, params=params, data=data)
    result = response.json()
    words_result = result.get('words_result', [])
    text = ' '.join([item['words'] for item in words_result])
    return text

def extract_order_number(text, patterns, filename):
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return match.group(1)  # 尝试返回捕获组内容
            except IndexError:
                try:
                    return match.group(0)  # 如果没有捕获组，返回整个匹配结果
                except IndexError:
                    return match.group()
    print(f"文件：{filename} 无匹配字段！")
    return None

def get_unique_filename(base_path, base_name, ext):
    counter = 1
    new_name = f"{base_name}{ext}"
    while os.path.exists(os.path.join(base_path, new_name)):
        new_name = f"{base_name}({counter}){ext}"
        counter += 1
    return new_name

def process_pdfs_in_folder(folder_path, patterns, api_key, secret_key, dpi):
    access_token = get_access_token(api_key, secret_key)
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(folder_path, filename)
        pdf_document = fitz.open(pdf_path)
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap(dpi=dpi)
        image_path = pdf_path.replace('.pdf', '_page1.png')
        pix.save(image_path)
        pdf_document.close()

        text = ocr_image(image_path, access_token)
        order_number = extract_order_number(text, patterns,filename)
        if order_number:
            sanitized_order_number = re.sub(r'[\\/*?:"<>|]', '_', order_number)
            new_pdf_name = get_unique_filename(folder_path, sanitized_order_number, '.pdf')
            new_pdf_path = os.path.join(folder_path, new_pdf_name)
            os.rename(pdf_path, new_pdf_path)

        os.remove(image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process PDF files to extract order numbers.')
    parser.add_argument('-f', '--folder_path', type=str, default=".\pdf", help='Path to the folder containing PDF files')
    parser.add_argument('-p', '--patterns', type=str, nargs='+', default=[r'订单号码([a-zA-Z0-9]+)', r'CG[a-zA-Z0-9]{10}', r'CG[a-zA-Z0-9]{8}'], help='List of regular expression patterns to extract order number')
    parser.add_argument('-a', '--api_key', type=str, default='xxx', help='Baidu OCR API key')
    parser.add_argument('-s', '--secret_key', type=str, default='xxx', help='Baidu OCR Secret key')
    parser.add_argument('-d', '--dpi', type=int, default=175, help='dip')

    args = parser.parse_args()

    BAIDU_OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

    process_pdfs_in_folder(args.folder_path, args.patterns, args.api_key, args.secret_key, args.dpi)
    input("处理完成。按任意键退出...")

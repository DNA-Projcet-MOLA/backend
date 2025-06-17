import pytesseract
from PIL import Image

def img2text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang="kor+eng")
        return text
    except Exception as e:
        print(f"[Text OCR] Error: {e}")
        return ""
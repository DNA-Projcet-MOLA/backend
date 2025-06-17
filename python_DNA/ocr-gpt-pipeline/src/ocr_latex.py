import sys
import os
sys.path.append(os.path.abspath("../LaTeX-OCR"))  # Latex-OCR 설치 경로 추가
#from im2latex import LatexOCR

# ocr_model = None

# def init_ocr():
#     global ocr_model
#     if ocr_model is None:
#         ocr_model = LatexOCR()
#     return ocr_model

# def img2latex(image_path):
#     model = init_ocr()
#     try:
#         return model.img2latex(image_path)
#     except Exception as e:
#         print(f"[LaTeX-OCR] Error: {e}")
#         return ""
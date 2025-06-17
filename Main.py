# Main.py

from PIL import Image
import pytesseract
import numpy as np

from SBERT_study import get_word_embeddings
from FAISS_study import find_similar_words

# Tesseract OCR 설정 (Windows 예시)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.TESSDATA_PREFIX = r"C:\Program Files\Tesseract-OCR"

def extract_text_from_image(image_path: str, lang: str = 'eng') -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang=lang)
    return text.strip()

def extract_keywords_from_text(text: str) -> list[str]:
    # 간단 예: 공백 기준 분리, 길이 2 이상인 토큰만
    tokens = text.split()
    return [t for t in tokens if len(t) > 1]

def generate_new_problem(similar_words: list[str]) -> str:
    return f"{', '.join(similar_words)}에 대해 설명하시오."

def main(image_path: str):
    # 1) OCR
    text = extract_text_from_image(image_path, lang='eng')
    print("추출된 텍스트:", text)

    # 2) 키워드 추출
    keywords = extract_keywords_from_text(text)
    print("추출된 키워드:", keywords)
    if not keywords:
        print("키워드를 추출하지 못했습니다.")
        return

    # 3) SBERT 임베딩
    embeddings = get_word_embeddings(keywords)
    print("임베딩 배열 형태:", embeddings.shape)

    # 4) FAISS 유사 단어 검색
    similar_lists = find_similar_words(keywords, embeddings, k=5)
    for kw, sims in zip(keywords, similar_lists):
        print(f"'{kw}'과(와) 유사한 단어:", sims)

    # 5) 첫 키워드 기반 새 문제 생성 예시
    first_sim = similar_lists[0]
    new_prob = generate_new_problem(first_sim)
    print("새로운 문제 예시:", new_prob)

if __name__ == "__main__":
    # 이미지 경로는 raw 문자열(r"…") 또는 '/' 사용
    image_path = r"C:\python_DNA\img\math_test_1.png"
    main(image_path)

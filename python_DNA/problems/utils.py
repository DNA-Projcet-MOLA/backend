import pytesseract
from PIL import Image

from pix2tex.cli import LatexOCR

import openai
import re
import json

# -------------------- OCR --------------------

ocr_model = None
def init_ocr():
    global ocr_model
    if ocr_model is None:
        ocr_model = LatexOCR()
    return ocr_model

def img2latex(image_path):
    model = init_ocr()
    try:
        return model(image_path)
    except Exception as e:
        print(f"[LaTeX-OCR] Error: {e}")
        return ""

def img2text(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang="kor+eng")
    except Exception as e:
        print(f"[Text OCR] Error: {e}")
        return ""

# -------------------- GPT 구조화 --------------------

OPENAI_API_KEY = "sk-..."  # ← 본인 키로 교체
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-4o"

def struct_problem_with_gpt(text, latex, image_path):
    prompt = f"""
아래는 실제 기출 또는 교재 수학 문제 이미지에서 OCR로 추출한 결과입니다.
[텍스트 OCR]
{text}

[수식(LaTeX)]
{latex}

[이미지 경로]
{image_path}

너는 수능·학평·모의고사·내신 기출 출제진 또는 고난도 수학 문제 데이터셋 분석 전문가야.
이 정보를 바탕으로, 아래 항목에 따라 **꼭 JSON으로** 문제 구조를 반환해.

필수 요구:
- 반드시 'question', 'latex', 'options', 'answer', 'category', 'image_path'로 명확하게 구분해.
- 각 항목에 상세한 내용을 담되, 수식, 기호, 변수, 단위, 한글/영어를 원본 그대로 복원해서 담아.
- options(보기가 없으면 빈 리스트 [])
- answer(정답이 명확치 않으면 추정 값이나 '모름', '없음' 등으로)
- latex(문제의 핵심 수식/조건 전체, OCR 결과가 부족하면 직접 복원해서 써도 됨)
- category(함수, 기하, 미적분, 확률, 통계, 수열, 논술, 기타 등 유형 예측)
- 기타 불확실한 정보도, 가능한 한 최대한 정보 손실 없이 구조화

반드시 아래 예시 형식(줄바꿈, 띄어쓰기 포함)을 따라줘.
예시:
{{
  "question": "실수 전체의 집합에서 연속인 함수 f(x)의 상수 a 값을 구하시오.",
  "latex": "f(x) = 5x + a (x < -2), f(x) = x^2 - a (x ≥ -2)",
  "options": ["1. 6", "2. 7", "3. 8", "4. 9", "5. 10"],
  "answer": "7",
  "category": "함수",
  "image_path": "{image_path}"
}}

JSON 이외의 불필요한 설명, 해설, 코멘트는 절대 붙이지 마.
항상 문제 정보를 완전히 JSON만으로, 한 번에 올바르게 반환해.
"""
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.0
    )
    content = response["choices"][0]["message"]["content"]
    try:
        json_data = re.search(r'\{[\s\S]+\}', content).group()
        data = json.loads(json_data)
        data["image_path"] = image_path
        return data
    except Exception as e:
        print("[GPT 구조화] Error parsing JSON:", e)
        return {
            "question": text,
            "latex": latex,
            "options": [],
            "answer": "",
            "category": "",
            "image_path": image_path
        }

# -------------------- 짧은 msg 생성 --------------------
def get_problem_msg(analysis):
    category = analysis.get('category', '수학')
    question = analysis.get('question', '')
    short_q = question[:30] + ("..." if len(question) > 30 else "")
    return f"[{category}] {short_q}"
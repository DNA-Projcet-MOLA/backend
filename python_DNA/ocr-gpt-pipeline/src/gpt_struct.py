import openai
import os

# OpenAI API 키는 환경변수로 저장, or config 파일에서 불러오기 권장
openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_MODEL = "gpt-4o"  # gpt-3.5-turbo도 가능, 성능 고려

def struct_problem_with_gpt(text, latex, image_path):
    prompt = f"""
아래는 수학 문제 이미지의 OCR 결과입니다.

[텍스트 OCR]
{text}

[수식(LaTeX)]
{latex}

위 정보를 바탕으로 실제 시험/기출/교재 스타일의 수학 문제로
문제, 보기, 정답, 조건, 수식, 이미지 경로를 아래와 같은 JSON 형식으로 정확하게 구조화해줘.
가능하면 문제 유형(예: 함수, 기하, 미적분 등)도 추론해줘.

예시:
{{
  "question": "...",
  "latex": "...",
  "options": ["...", "...", "..."],
  "answer": "...",
  "category": "...",
  "image_path": "..."
}}

실제 데이터만 JSON으로 반환해줘.
"""
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.0
    )
    content = response.choices[0].message.content
    # content에서 JSON 파싱 (필요시 ast.literal_eval, json.loads 등 후처리)
    import json, re
    try:
        # JSON 부분만 추출
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
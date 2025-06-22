import os, json, random, re, traceback
from django.conf import settings
from .resources import PROBLEM_MAKERS, classify_type_by_text
from .faiss_search import get_similar_problem_idxs, load_problems
import openai
from PIL import Image, ImageDraw, ImageFont

from dotenv import load_dotenv
load_dotenv()

def save_ai_problem_image(img_object, prefix='ai_problem'):
    # media/images/에 저장
    os.makedirs(settings.IMAGES_DIR, exist_ok=True)
    filename = f"{prefix}_{random.randint(100000,999999)}.png"
    image_path = settings.IMAGES_DIR / filename
    img_object.save(image_path)
    image_url = f"/media/images/{filename}"
    return image_path, image_url

def append_problem_to_json(data):
    os.makedirs(settings.PROBLEM_JSON_DIR, exist_ok=True)
    problems_json_path = settings.PROBLEM_JSON_PATH
    if os.path.exists(problems_json_path):
        with open(problems_json_path, "r", encoding="utf-8") as f:
            problems = json.load(f)
    else:
        problems = []
    problems.append(data)
    with open(problems_json_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

def make_problem_with_gpt_service(problem_type, top_k=3):
    # 1. 문제 예시 추출
    problems = load_problems()
    similar_idxs = [i for i, p in enumerate(problems)
                    if classify_type_by_text(p['question'] + str(p.get('latex', ''))) == problem_type]
    similar_problems = [problems[idx] for idx in (random.sample(similar_idxs, min(top_k, len(similar_idxs))) if similar_idxs else random.sample(range(len(problems)), min(top_k, len(problems))))]

    # 2. 유형 랜덤 문제 하나 생성
    problem_base = PROBLEM_MAKERS[problem_type]()
    def extract_latex_and_explain(latex_data):
        if isinstance(latex_data, list):
            latex_conds = [l for l in latex_data if re.search(r'[=<>\\]', l)]
            explain = ' '.join([l for l in latex_data if not re.search(r'[=<>\\]', l)])
            return latex_conds[:3], explain
        return [], ""
    examples = []
    for prob in similar_problems:
        latex_conds, ex_explain = extract_latex_and_explain(prob.get('latex', ''))
        examples.append({
            "question": prob.get('question', ''),
            "latex": latex_conds,
            "explain": ex_explain
        })
    latex_conds, explain = extract_latex_and_explain(problem_base['latex'])

    # 3. GPT 프롬프트 생성
    def make_gpt_problem_prompt(type_name, answer, latex_conds, examples, explain):
        prompt = (
            "[문제 생성 지침]\n"
            "1. 반드시 'tikz_code' 필드를 포함해, 필요한 경우 LaTeX tikzpicture 코드를 직접 반환하세요.\n"
            "2. 예시문제 형식, latex, 설명, 수식 등을 우선 반영하세요. 정답(answer)은 반드시 {answer}입니다.\n"
            "3. 반환 JSON 구조: {{'question':..., 'latex':..., 'explain':..., 'tikz_code':... (필요시)}}\n"
            "------\n"
        ).format(type_name=type_name, answer=answer)
        for i, ex in enumerate(examples):
            ex_latex, ex_explain = ex.get('latex', []), ex.get('explain', '')
            prompt += f"\n예시 {i+1}: {ex['question']} | 조건: {', '.join(ex_latex)}"
            if ex_explain: prompt += f" | 설명: {ex_explain}"
        prompt += (
            f"\n------\n"
            f"[참고] 유형명: {type_name}\n"
            f"[참고] latex 조건 예시: {', '.join(latex_conds)}\n"
            f"[참고] 설명 예시: {explain}\n"
            f"tikz_code 예시: (함수 그래프/도형 등 tikzpicture 전체)\n"
            f"JSON만 반환하세요."
        )
        return prompt

    def safe_json_loads(content):
        m = re.search(r'\{[\s\S]+\}', content)
        if not m:
            raise ValueError("No JSON block found.")
        return json.loads(m.group())

    # 4. GPT 호출
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = make_gpt_problem_prompt(problem_type, problem_base['answer'], latex_conds, examples, explain)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=850,
        temperature=0.5
    )
    content = response.choices[0].message.content
    try:
        p = safe_json_loads(content)
        if not p.get('latex'): p['latex'] = latex_conds
        if not p.get('question'): p['question'] = f"{problem_type} 유형 고난도 문제"
        if not p.get('explain'): p['explain'] = explain

        # 5. (예시) 문제 텍스트 이미지로 저장
        img = Image.new('RGB', (700, 160), (255,255,255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((20, 30), p['question'], fill=(0,0,0), font=font)
        image_path, image_url = save_ai_problem_image(img)

        # 6. 저장 및 응답
        p['image_path'] = image_url
        append_problem_to_json(p)
        return p
    except Exception as e:
        print("[ERROR] GPT 문제 파싱 실패!")
        print("에러 내용:", str(e))
        traceback.print_exc()
        return None
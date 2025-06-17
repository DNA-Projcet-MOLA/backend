import openai
import base64

api_key = "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"  # 본인의 OpenAI API Key

client = openai.OpenAI(api_key=api_key)

def gpt_image_structured_problem_analysis(image_path, client):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    prompt = (
        "이 이미지는 수학, 국어, 영어, 과학, 사회 문제 중 하나입니다. "
        "1) 조건(수식, 문장 포함)을 한 줄씩 나열, "
        "2) 문제 질문을 한 줄로 요약, "
        "3) 보기가 있다면 번호별로 정리. "
        "수식·기호·변수명이 깨지지 않게 복원해줘."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_data}"}
                    }
                ],
            }
        ],
        max_tokens=2048,
        temperature=0.1,
    )
    return response.choices[0].message.content

image_path = r"C:\python_DNA\img\math_test_2.png"
result = gpt_image_structured_problem_analysis(image_path, client)
print(result)

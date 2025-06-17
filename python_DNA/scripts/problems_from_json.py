import os, django, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_DNA.settings")
django.setup()

from problems.models import Problem

def main():
    with open('ocr_gpt_pipeline/results/problems.json', encoding='utf-8') as f:
        problems = json.load(f)
    for item in problems:
        # 예시: item = {"title": "...", "content": "...", "latex": "...", "answer": "...", "image": "...", ...}
        obj, created = Problem.objects.get_or_create(
            title=item["title"],
            defaults={
                "content": item.get("content") or item.get("latex", ""),
                "subject": item.get("subject", ""),
                "level": item.get("level", 1),
                "latex": item.get("latex", ""),
                "answer": item.get("answer", ""),
                "tags": ",".join(item.get("tags", [])),
                # image 경로는 필요에 따라 media/problems/로 복사
            }
        )
        print(f"등록: {obj} ({'신규' if created else '중복'})")

if __name__ == "__main__":
    main()
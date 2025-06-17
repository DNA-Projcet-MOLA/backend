from django.db import models

class Problem(models.Model):
    title = models.CharField("문제 제목", max_length=200)
    content = models.TextField("문제 본문")
    image = models.ImageField("문제 이미지", upload_to='problems/', null=True, blank=True)
    subject = models.CharField("과목", max_length=20, blank=True)
    level = models.PositiveSmallIntegerField("난이도", null=True, blank=True)
    latex = models.TextField("LaTeX 코드", blank=True)           # OCR 결과 (optional)
    answer = models.TextField("정답/해설", blank=True)           # GPT 생성 결과 (optional)
    tags = models.CharField("태그", max_length=100, blank=True)  # GPT, 사용자 라벨
    created_at = models.DateField("출제일", auto_now_add=True)

    def __str__(self):
        return f"[{self.subject}] {self.title}"
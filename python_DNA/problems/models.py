from django.db import models
from users.models import User

class Problem(models.Model):
    question = models.TextField("문제 내용", null=True, blank=True, default="")
    image_path = models.CharField("문제 이미지 경로", max_length=255, null=True, blank=True, default="")
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자", null=True, blank=True)

    def __str__(self):
        return self.question[:50]

from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_path(instance, filename):
    return f"avatars/{instance.username}/{filename}"

class User(AbstractUser):
    email = models.EmailField("이메일", unique=True, blank=False)
    real_name = models.CharField("이름", max_length=30)
    birthdate = models.DateField("생년월일", null=True, blank=True)
    school = models.CharField("학교명", max_length=50, blank=True)
    student_number = models.PositiveSmallIntegerField("학번", null=True, blank=True)
    avatar = models.ImageField("프로필 사진", upload_to=user_avatar_path, null=True, blank=True, default="avatars/default.jpg")

    REQUIRED_FIELDS = ['email', 'real_name', 'birthdate', 'school', 'student_number']
    # grade, classroom 제거

    class Meta:
        unique_together = [('school', 'student_number')]  # 고유 제약: 학교+학번

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatars/default.jpg'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.real_name})"

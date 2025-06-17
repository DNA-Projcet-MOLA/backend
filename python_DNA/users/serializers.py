from rest_framework import serializers
from .models import User
from django.utils import timezone

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "real_name", "birthdate",
                  "school", "grade", "classroom", "student_number", "avatar")
        extra_kwargs = {
            "real_name": {"required": True},
            "birthdate": {"required": True},
            "school": {"required": True},
            "grade": {"required": True},
            "classroom": {"required": True},
            "student_number": {"required": True},
        }

    def validate_birthdate(self, value):
        today = timezone.now().date()
        age = (today - value).days // 365
        if not (7 <= age <= 21):
            raise serializers.ValidationError("생년월일을 정확히 입력하세요. (7~21세만 가입 가능)")
        return value

    def validate_grade(self, value):
        if not (1 <= value <= 3):
            raise serializers.ValidationError("학년은 1~3 사이여야 합니다.")
        return value

    def validate_classroom(self, value):
        if not (1 <= value <= 20):
            raise serializers.ValidationError("반은 1~20 사이여야 합니다.")
        return value

    def validate_student_number(self, value):
        if not (1 <= value <= 50):
            raise serializers.ValidationError("학번은 1~50 사이여야 합니다.")
        return value

    def validate(self, data):
        qs = User.objects.filter(
            school=data['school'],
            grade=data['grade'],
            classroom=data['classroom'],
            student_number=data['student_number'],
        )
        if qs.exists():
            raise serializers.ValidationError("이미 등록된 학번입니다.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        if not user.avatar:
            user.avatar = 'avatars/default.jpg'
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "real_name", "birthdate", "email", "school", "grade", "classroom", "student_number", "avatar")
        read_only_fields = ("id", "username", "avatar", "email")

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("real_name", "birthdate", "school", "grade", "classroom", "student_number", "avatar")

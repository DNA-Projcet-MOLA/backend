from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='비밀번호 확인')
    avatar = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'real_name',
            'birthdate',
            'school',
            'student_number',
            'password',
            'password2',
            'avatar',   # 추가됨
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        avatar = validated_data.pop('avatar', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            real_name=validated_data.get('real_name', ''),
            birthdate=validated_data.get('birthdate', None),
            school=validated_data.get('school', ''),
            student_number=validated_data.get('student_number', None),
            password=validated_data['password'],
        )
        if avatar:
            user.avatar = avatar
            user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'real_name',
            'birthdate',
            'school',
            'student_number',
            'avatar',
        ]
        # read_only_fields = []  # 완전히 제거

    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token['real_name'] = user.real_name
        token['email'] = user.email
        token['avatar'] = user.avatar.url if user.avatar else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username,
            'real_name': self.user.real_name,
            'email': self.user.email,
            'avatar': self.user.avatar.url if self.user.avatar else None,
        }
        return data


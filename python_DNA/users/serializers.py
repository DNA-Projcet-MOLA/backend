from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    사용자 회원가입을 위한 시리얼라이저
    
    새로운 사용자 계정 생성을 위한 모든 필수 정보를 검증하고 처리합니다.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        help_text="비밀번호 (최소 8자, 숫자와 문자 조합 권장)"
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        label='비밀번호 확인',
        help_text="비밀번호 확인 (위 비밀번호와 일치해야 함)"
    )
    avatar = serializers.ImageField(
        required=False, 
        allow_null=True, 
        allow_empty_file=True,
        help_text="프로필 사진 (선택사항, JPG/PNG 형식 권장)"
    )

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
    """
    사용자 프로필 관리를 위한 시리얼라이저
    
    로그인한 사용자의 프로필 정보 조회, 수정을 위한 시리얼라이저입니다.
    """
    
    username = serializers.CharField(
        help_text="사용자 아이디 (고유값, 중복 불가)"
    )
    email = serializers.EmailField(
        help_text="이메일 주소 (고유값, 중복 불가)"
    )
    real_name = serializers.CharField(
        help_text="실명"
    )
    birthdate = serializers.DateField(
        help_text="생년월일 (YYYY-MM-DD 형식)"
    )
    school = serializers.CharField(
        help_text="학교명"
    )
    student_number = serializers.IntegerField(
        help_text="학번"
    )
    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="프로필 사진 (선택사항, JPG/PNG 형식 권장)"
    )
    
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


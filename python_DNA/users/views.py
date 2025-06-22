from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer, MyTokenObtainPairSerializer
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

class UserRegisterView(generics.CreateAPIView):
    """
    사용자 회원가입 API
    
    새로운 사용자 계정을 생성합니다.
    """
    serializer_class = UserRegisterSerializer
    
    @swagger_auto_schema(
        operation_summary="회원가입",
        operation_description="""새로운 사용자 계정을 생성합니다.
        
모든 필수 필드를 포함하여 요청해야 합니다:
- username: 사용자 아이디 (고유값)
- email: 이메일 주소 (고유값)
- real_name: 실명
- birthdate: 생년월일 (YYYY-MM-DD 형식)
- school: 학교명
- student_number: 학번
- password: 비밀번호
- password2: 비밀번호 확인
- avatar: 프로필 사진 (선택사항)
        """,
        tags=["사용자 인증"],
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "real_name": "홍길동",
                        "birthdate": "2000-01-01",
                        "school": "선린인터넷고등학교",
                        "student_number": 1001,
                        "avatar": "/media/avatars/john_doe/profile.jpg"
                    }
                }
            ),
            400: openapi.Response(
                description="유효하지 않은 데이터",
                examples={
                    "application/json": {
                        "username": ["이미 사용 중인 아이디입니다."],
                        "email": ["이미 사용 중인 이메일입니다."],
                        "password": ["비밀번호와 비밀번호 확인이 일치하지 않습니다."]
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    사용자 로그인 API
    
    사용자 인증 후 JWT 액세스 토큰과 리프레시 토큰을 발급합니다.
    """
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = []
    
    @swagger_auto_schema(
        operation_summary="로그인",
        operation_description="""사용자 인증을 통해 JWT 토큰을 발급받습니다.
        
성공 시 액세스 토큰과 리프레시 토큰, 사용자 정보를 반환합니다.
액세스 토큰은 API 요청 시 Authorization 헤더에 포함해야 합니다.
        """,
        tags=["사용자 인증"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="사용자 아이디",
                    example="john_doe"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="비밀번호",
                    example="password123"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "username": "john_doe",
                            "real_name": "홍길동",
                            "email": "john@example.com",
                            "avatar": "/media/avatars/john_doe/profile.jpg"
                        }
                    }
                }
            ),
            401: openapi.Response(
                description="인증 실패",
                examples={
                    "application/json": {
                        "detail": "제공된 자격 증명으로 로그인할 수 없습니다."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    사용자 프로필 관리 API
    
    현재 로그인한 사용자의 프로필 정보를 조회, 수정, 삭제할 수 있습니다.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

    @swagger_auto_schema(
        operation_summary="프로필 조회",
        operation_description="현재 로그인한 사용자의 프로필 정보를 조회합니다.",
        tags=["사용자 프로필"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="프로필 조회 성공",
                examples={
                    "application/json": {
                        "username": "john_doe",
                        "email": "john@example.com",
                        "real_name": "홍길동",
                        "birthdate": "2000-01-01",
                        "school": "선린인터넷고등학교",
                        "student_number": 1001,
                        "avatar": "/media/avatars/john_doe/profile.jpg"
                    }
                }
            ),
            401: openapi.Response(
                description="인증 실패",
                examples={
                    "application/json": {
                        "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="프로필 부분 수정",
        operation_description="""현재 로그인한 사용자의 프로필 정보를 부분적으로 수정합니다.
        
수정하고자 하는 필드만 전송하면 됩니다.
아바타 이미지는 multipart/form-data 형식으로 전송해야 합니다.
        """,
        tags=["사용자 프로필"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="프로필 수정 성공",
                examples={
                    "application/json": {
                        "username": "john_doe",
                        "email": "john@example.com",
                        "real_name": "홍길동",
                        "birthdate": "2000-01-01",
                        "school": "선린인터넷고등학교",
                        "student_number": 1001,
                        "avatar": "/media/avatars/john_doe/new_profile.jpg"
                    }
                }
            ),
            400: openapi.Response(
                description="유효하지 않은 데이터",
                examples={
                    "application/json": {
                        "username": ["이미 사용 중인 아이디입니다."],
                        "email": ["올바른 이메일 주소를 입력하세요."]
                    }
                }
            ),
            401: openapi.Response(
                description="인증 실패",
                examples={
                    "application/json": {
                        "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
                    }
                }
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="프로필 전체 수정",
        operation_description="""현재 로그인한 사용자의 프로필 정보를 전체적으로 수정합니다.
        
모든 필드를 전송해야 합니다.
아바타 이미지는 multipart/form-data 형식으로 전송해야 합니다.
        """,
        tags=["사용자 프로필"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="프로필 수정 성공",
                examples={
                    "application/json": {
                        "username": "john_doe",
                        "email": "john@example.com",
                        "real_name": "홍길동",
                        "birthdate": "2000-01-01",
                        "school": "선린인터넷고등학교",
                        "student_number": 1001,
                        "avatar": "/media/avatars/john_doe/updated_profile.jpg"
                    }
                }
            ),
            400: openapi.Response(
                description="유효하지 않은 데이터",
                examples={
                    "application/json": {
                        "username": ["이 필드는 필수입니다."],
                        "email": ["올바른 이메일 주소를 입력하세요."]
                    }
                }
            ),
            401: openapi.Response(
                description="인증 실패",
                examples={
                    "application/json": {
                        "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
                    }
                }
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="회원탈퇴",
        operation_description="현재 로그인한 사용자의 계정을 삭제합니다. 이 작업은 되돌릴 수 없습니다.",
        tags=["사용자 프로필"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            204: openapi.Response(
                description="회원탈퇴 성공",
                examples={
                    "application/json": {
                        "detail": "회원탈퇴가 완료되었습니다."
                    }
                }
            ),
            401: openapi.Response(
                description="인증 실패",
                examples={
                    "application/json": {
                        "detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
                    }
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user

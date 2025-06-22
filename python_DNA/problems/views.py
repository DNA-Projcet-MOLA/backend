import os
import json
from uuid import uuid4

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Problem
from .serializer import ProblemSerializer

# --- 분석 함수 utils에서 가져오기
from .utils import img2text, img2latex, struct_problem_with_gpt, get_problem_msg

class ProblemImageUploadAPIView(APIView):
    """
    수학 문제 이미지 업로드 및 분석 API
    
    업로드된 이미지를 OCR과 AI를 통해 분석하여 수학 문제로 구조화합니다.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="수학 문제 이미지 업로드 및 분석",
        operation_description="""이미지 파일을 업로드하여 수학 문제를 분석하고 구조화합니다.
        
처리 과정:
1. 이미지 파일 저장
2. OCR을 통한 텍스트 추출
3. LaTeX 수식 변환
4. GPT를 통한 문제 구조화 분석
5. 데이터베이스 저장
6. JSON 파일 백업 저장

지원 이미지 형식: JPG, PNG, GIF, BMP, TIFF
최대 파일 크기: 10MB
        """,
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="분석할 수학 문제 이미지 파일",
                type=openapi.TYPE_FILE,
                required=True,
            )
        ],
        consumes=['multipart/form-data'],
        responses={
            201: openapi.Response(
                description="이미지 업로드 및 분석 성공",
                examples={
                    "application/json": {
                        "msg": "문제가 성공적으로 분석되었습니다.",
                        "problem": {
                            "id": 1,
                            "question": "다음 방정식을 풀어보세요: x² + 5x + 6 = 0",
                            "image_path": "/media/images/abc123def456.jpg",
                            "created_at": "2024-01-01T12:00:00Z",
                            "user": 1
                        },
                        "analysis": {
                            "question": "다음 방정식을 풀어보세요: x² + 5x + 6 = 0",
                            "latex": "x^2 + 5x + 6 = 0",
                            "options": ["A) x = -2, -3", "B) x = 2, 3", "C) x = -1, -6", "D) x = 1, 6"],
                            "answer": "A) x = -2, -3",
                            "category": "이차방정식"
                        },
                        "image_url": "/media/images/abc123def456.jpg",
                        "created_at": "2024-01-01T12:00:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "error": "이미지 파일이 필요합니다."
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
            ),
            413: openapi.Response(
                description="파일 크기 초과",
                examples={
                    "application/json": {
                        "error": "파일 크기가 너무 큽니다. 최대 10MB까지 업로드 가능합니다."
                    }
                }
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "error": "이미지 분석 중 오류가 발생했습니다."
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "이미지 파일이 필요합니다."}, status=400)

        # 1. 이미지 저장
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'), exist_ok=True)
        ext = os.path.splitext(image.name)[-1]
        filename = f"{uuid4().hex}{ext}"
        image_save_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
        with open(image_save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        image_url = f"/media/images/{filename}"

        # 2. OCR/AI 분석
        text = img2text(image_save_path)
        latex = img2latex(image_save_path)
        analysis = struct_problem_with_gpt(text, latex, image_url)

        # 3. DB 저장
        problem = Problem.objects.create(
            question=analysis['question'],
            image_path=image_url,
            user=request.user
        )

        # 4. JSON 파일 저장
        problem_json_dir = os.path.join(settings.BASE_DIR, 'problem_json')
        os.makedirs(problem_json_dir, exist_ok=True)
        problems_json_path = os.path.join(problem_json_dir, 'problems.json')
        if os.path.exists(problems_json_path):
            with open(problems_json_path, 'r', encoding='utf-8') as f:
                problems = json.load(f)
        else:
            problems = []
        info = analysis.copy()
        info['user'] = request.user.username
        problems.append(info)
        with open(problems_json_path, 'w', encoding='utf-8') as f:
            json.dump(problems, f, ensure_ascii=False, indent=2)

        serializer = ProblemSerializer(problem)
        msg = get_problem_msg(analysis)

        return Response({
            "msg": msg,
            "problem": serializer.data,
            "analysis": {
                "question": analysis['question'],
                "latex": analysis['latex'],
                "options": analysis.get('options', []),
                "answer": analysis.get('answer', ''),
                "category": analysis.get('category', '')
            },
            "image_url": image_url,
            "created_at": problem.created_at
        }, status=201)

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    """
    수학 문제 목록 조회 및 생성 API
    
    모든 수학 문제 목록을 최신순으로 조회하거나 새로운 문제를 직접 생성할 수 있습니다.
    """
    queryset = Problem.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="수학 문제 목록 조회",
        operation_description="등록된 모든 수학 문제 목록을 최신순으로 조회합니다.",
        tags=["수학 문제 관리"],
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
                description="문제 목록 조회 성공",
                examples={
                    "application/json": [
                        {
                            "id": 2,
                            "question": "다음 적분을 계산하세요: ∫(x² + 2x + 1)dx",
                            "image_path": "/media/images/def456ghi789.jpg",
                            "created_at": "2024-01-02T14:30:00Z",
                            "user": 1
                        },
                        {
                            "id": 1,
                            "question": "다음 방정식을 풀어보세요: x² + 5x + 6 = 0",
                            "image_path": "/media/images/abc123def456.jpg",
                            "created_at": "2024-01-01T12:00:00Z",
                            "user": 1
                        }
                    ]
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
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="수학 문제 직접 생성",
        operation_description="""이미지 없이 텍스트로 수학 문제를 직접 생성합니다.
        
이미지 업로드 API와 달리 문제 텍스트만으로 문제를 등록할 수 있습니다.
자동 분석 없이 사용자가 입력한 내용 그대로 저장됩니다.
        """,
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['question'],
            properties={
                'question': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="수학 문제 내용",
                    example="삼각함수 sin(30°)의 값을 구하시오."
                ),
                'image_path': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="문제 이미지 경로 (선택사항)",
                    example="/media/images/custom_problem.jpg"
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="문제 생성 성공",
                examples={
                    "application/json": {
                        "id": 3,
                        "question": "삼각함수 sin(30°)의 값을 구하시오.",
                        "image_path": "",
                        "created_at": "2024-01-03T10:15:00Z",
                        "user": 1
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "question": ["이 필드는 필수입니다."]
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProblemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    특정 수학 문제 상세 조회, 수정, 삭제 API
    
    문제 ID를 통해 특정 문제의 상세 정보를 조회, 수정, 삭제할 수 있습니다.
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="수학 문제 상세 조회",
        operation_description="문제 ID를 통해 특정 수학 문제의 상세 정보를 조회합니다.",
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="조회할 문제의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="문제 상세 조회 성공",
                examples={
                    "application/json": {
                        "id": 1,
                        "question": "다음 방정식을 풀어보세요: x² + 5x + 6 = 0",
                        "image_path": "/media/images/abc123def456.jpg",
                        "created_at": "2024-01-01T12:00:00Z",
                        "user": 1
                    }
                }
            ),
            404: openapi.Response(
                description="문제를 찾을 수 없음",
                examples={
                    "application/json": {
                        "detail": "찾을 수 없습니다."
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
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="수학 문제 수정",
        operation_description="문제 ID를 통해 특정 수학 문제의 정보를 수정합니다.",
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="수정할 문제의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="수정할 문제 내용",
                    example="다음 방정식을 풀어보세요: x² + 3x + 2 = 0"
                ),
                'image_path': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="수정할 이미지 경로",
                    example="/media/images/updated_problem.jpg"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="문제 수정 성공",
                examples={
                    "application/json": {
                        "id": 1,
                        "question": "다음 방정식을 풀어보세요: x² + 3x + 2 = 0",
                        "image_path": "/media/images/updated_problem.jpg",
                        "created_at": "2024-01-01T12:00:00Z",
                        "user": 1
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "question": ["이 필드는 공백일 수 없습니다."]
                    }
                }
            ),
            404: openapi.Response(
                description="문제를 찾을 수 없음",
                examples={
                    "application/json": {
                        "detail": "찾을 수 없습니다."
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
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="수학 문제 부분 수정",
        operation_description="문제 ID를 통해 특정 수학 문제의 일부 정보를 수정합니다.",
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="수정할 문제의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="수정할 문제 내용",
                    example="다음 방정식을 풀어보세요: x² + 3x + 2 = 0"
                ),
                'image_path': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="수정할 이미지 경로",
                    example="/media/images/updated_problem.jpg"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="문제 부분 수정 성공",
                examples={
                    "application/json": {
                        "id": 1,
                        "question": "다음 방정식을 풀어보세요: x² + 3x + 2 = 0",
                        "image_path": "/media/images/abc123def456.jpg",
                        "created_at": "2024-01-01T12:00:00Z",
                        "user": 1
                    }
                }
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "question": ["이 필드는 공백일 수 없습니다."]
                    }
                }
            ),
            404: openapi.Response(
                description="문제를 찾을 수 없음",
                examples={
                    "application/json": {
                        "detail": "찾을 수 없습니다."
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
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="수학 문제 삭제",
        operation_description="문제 ID를 통해 특정 수학 문제를 삭제합니다. 이 작업은 되돌릴 수 없습니다.",
        tags=["수학 문제 관리"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT 액세스 토큰 (예: Bearer eyJ0eXAiOiJKV1Q...)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="삭제할 문제의 ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            204: openapi.Response(
                description="문제 삭제 성공",
                examples={}
            ),
            404: openapi.Response(
                description="문제를 찾을 수 없음",
                examples={
                    "application/json": {
                        "detail": "찾을 수 없습니다."
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
        return super().delete(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
from .utils.generator import make_problem_with_gpt_service
from .utils.resources import PROBLEM_MAKERS

class GenerateAiProblemAPIView(APIView):
    """
    AI 기반 수학 문제 생성 API
    
    GPT를 활용하여 다양한 유형의 수학 문제를 자동으로 생성합니다.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="AI 수학 문제 생성 (GET)",
        operation_description="""랜덤하게 선택된 수학 문제 유형에 따라 AI가 새로운 문제를 생성합니다.
        
지원되는 문제 유형:
- 이차방정식
- 삼각함수
- 미적분
- 대수
- 기하
- 확률통계

각 요청마다 다른 유형의 문제가 랜덤하게 생성됩니다.
        """,
        tags=["AI 문제 생성"],
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
                description="AI 문제 생성 성공",
                examples={
                    "application/json": {
                        "problem_type": "이차방정식",
                        "question": "다음 이차방정식을 풀어보세요: 2x² - 7x + 3 = 0",
                        "latex": "2x^2 - 7x + 3 = 0",
                        "options": [
                            "A) x = 3, x = 1/2",
                            "B) x = -3, x = -1/2", 
                            "C) x = 2, x = 3/2",
                            "D) x = -2, x = -3/2"
                        ],
                        "answer": "A) x = 3, x = 1/2",
                        "explanation": "인수분해를 사용하면: (2x-1)(x-3) = 0이므로 x = 1/2 또는 x = 3입니다.",
                        "difficulty": "medium",
                        "category": "대수",
                        "created_at": "2024-01-01T15:30:00Z"
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
            500: openapi.Response(
                description="AI 문제 생성 실패",
                examples={
                    "application/json": {
                        "error": "문제 생성 실패"
                    }
                }
            )
        }
    )
    def get(self, request):
        problem_types = list(PROBLEM_MAKERS.keys())
        problem_type = random.choice(problem_types)
        result = make_problem_with_gpt_service(problem_type, top_k=3)
        if result:
            return Response(result)
        else:
            return Response({'error': '문제 생성 실패'}, status=500)

    @swagger_auto_schema(
        operation_summary="AI 수학 문제 생성 (POST)",
        operation_description="""랜덤하게 선택된 수학 문제 유형에 따라 AI가 새로운 문제를 생성합니다.
        
GET과 동일한 기능을 수행하나, POST 메소드를 선호하는 클라이언트를 위해 제공됩니다.
추후 특정 문제 유형 지정, 난이도 설정 등의 옵션을 추가할 예정입니다.
        """,
        tags=["AI 문제 생성"],
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
            properties={
                'problem_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="생성할 문제 유형 (선택사항, 비어있으면 랜덤 선택)",
                    example="이차방정식",
                    enum=["이차방정식", "삼각함수", "미적분", "대수", "기하", "확률통계"]
                ),
                'difficulty': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="문제 난이도 (선택사항)",
                    example="medium",
                    enum=["easy", "medium", "hard"]
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="AI 문제 생성 성공",
                examples={
                    "application/json": {
                        "problem_type": "삼각함수",
                        "question": "다음 삼각함수의 값을 구하세요: sin(45°) + cos(60°)",
                        "latex": "\\sin(45^\\circ) + \\cos(60^\\circ)",
                        "options": [
                            "A) 1 + √2/2",
                            "B) √2/2 + 1/2",
                            "C) 1/2 + √3/2",
                            "D) √3/2 + √2/2"
                        ],
                        "answer": "B) √2/2 + 1/2",
                        "explanation": "sin(45°) = √2/2, cos(60°) = 1/2이므로 답은 √2/2 + 1/2입니다.",
                        "difficulty": "medium",
                        "category": "삼각함수",
                        "created_at": "2024-01-01T15:30:00Z"
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
            500: openapi.Response(
                description="AI 문제 생성 실패",
                examples={
                    "application/json": {
                        "error": "문제 생성 실패"
                    }
                }
            )
        }
    )
    def post(self, request):
        return self.get(request)

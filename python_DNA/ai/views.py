from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random
from .utils.generator import make_problem_with_gpt_service
from .utils.resources import PROBLEM_MAKERS

class GenerateAiProblemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        problem_types = list(PROBLEM_MAKERS.keys())
        problem_type = random.choice(problem_types)
        result = make_problem_with_gpt_service(problem_type, top_k=3)
        if result:
            return Response(result)
        else:
            return Response({'error': '문제 생성 실패'}, status=500)

    def post(self, request):
        return self.get(request)
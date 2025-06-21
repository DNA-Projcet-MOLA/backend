import os
import json
from uuid import uuid4

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, permissions

from django.conf import settings

from .models import Problem
from .serializer import ProblemSerializer

# --- 분석 함수 utils에서 가져오기
from .utils import img2text, img2latex, struct_problem_with_gpt, get_problem_msg

class ProblemImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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

# 나머지 CRUD API
class ProblemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProblemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
from rest_framework import serializers
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    """
    수학 문제 데이터 처리를 위한 시리얼라이저
    
    수학 문제의 생성, 조회, 수정, 삭제를 위한 데이터 직렬화/역직렬화를 담당합니다.
    """
    
    id = serializers.IntegerField(
        read_only=True,
        help_text="문제 고유 ID (자동 생성)"
    )
    question = serializers.CharField(
        max_length=None,
        help_text="수학 문제 내용 (텍스트 형식)"
    )
    image_path = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="문제 이미지 파일 경로 (선택사항)"
    )
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="문제 등록 일시 (자동 생성)"
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        help_text="문제 작성자 ID (자동 설정)"
    )
    
    class Meta:
        model = Problem
        fields = ['id', 'question', 'image_path', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

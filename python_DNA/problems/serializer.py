from rest_framework import serializers
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'question', 'image_path', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

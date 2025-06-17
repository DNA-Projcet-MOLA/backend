from rest_framework import serializers
from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'title', 'content', 'image', 'subject', 'level', 'latex', 'answer', 'tags', 'created_at')
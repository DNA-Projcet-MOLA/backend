from rest_framework import generics
from .models import Problem
from .serializer import ProblemSerializer

class ProblemListAPI(generics.ListAPIView):
    queryset = Problem.objects.all().order_by('-created_at')
    serializer_class = ProblemSerializer

class ProblemDetailAPI(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
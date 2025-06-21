from django.urls import path
from .views import (
    ProblemImageUploadAPIView,
    ProblemListCreateAPIView,
    ProblemRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('upload/', ProblemImageUploadAPIView.as_view(), name='problem-image-upload'),
    path('list/', ProblemListCreateAPIView.as_view(), name='problem-list-create'),
    path('<int:pk>/', ProblemRetrieveUpdateDestroyAPIView.as_view(), name='problem-detail'),
]
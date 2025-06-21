from django.urls import path
from .views import GenerateAiProblemAPIView

urlpatterns = [
    path('generate/', GenerateAiProblemAPIView.as_view(), name='ai-generate'),
]
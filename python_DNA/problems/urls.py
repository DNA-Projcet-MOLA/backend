from django.urls import path
from .views import ProblemListAPI, ProblemDetailAPI

urlpatterns = [
    path('list/', ProblemListAPI.as_view(), name='problem-list'),
    path('<int:pk>/', ProblemDetailAPI.as_view(), name='problem-detail'),
]
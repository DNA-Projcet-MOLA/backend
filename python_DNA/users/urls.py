from django.urls import path
from .views import UserRegisterView, MyTokenObtainPairView, UserProfileView

urlpatterns = [
    path('api/signup/', UserRegisterView.as_view(), name='user-signup'),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
]

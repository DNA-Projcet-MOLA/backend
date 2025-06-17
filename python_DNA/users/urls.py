from django.urls import path
from .views import SignUpAPI, ProfileAPI, ProfileUpdateAPI, CheckDuplicateAPI

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='user-signup'),
    path('me/', ProfileAPI.as_view(), name='my-profile'),
    path('me/update/', ProfileUpdateAPI.as_view(), name='my-profile-update'),
    path('check/', CheckDuplicateAPI.as_view(), name='user-duplicate-check'),
]

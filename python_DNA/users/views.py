from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer, MyTokenObtainPairSerializer
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = []


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()  # 이 한 줄 추가

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT access token, 예시: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT access token, 예시: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT access token, 예시: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT access token, 예시: Bearer {token}",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response({"detail": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


    def get_object(self):
        return self.request.user
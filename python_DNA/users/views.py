from rest_framework import generics, permissions, status, parsers, views
from rest_framework.response import Response
from .models import User
from .serializers import SignUpSerializer, UserSerializer, UserUpdateSerializer

class SignUpAPI(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

class ProfileAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class ProfileUpdateAPI(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    def get_object(self):
        return self.request.user

class CheckDuplicateAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username")
        email = request.GET.get("email")
        school = request.GET.get("school")
        grade = request.GET.get("grade")
        classroom = request.GET.get("classroom")
        student_number = request.GET.get("student_number")
        data = {}
        if username:
            data["username_exists"] = User.objects.filter(username=username).exists()
        if email:
            data["email_exists"] = User.objects.filter(email=email).exists()
        if school and grade and classroom and student_number:
            data["student_number_exists"] = User.objects.filter(
                school=school, grade=grade, classroom=classroom, student_number=student_number
            ).exists()
        return Response(data, status=status.HTTP_200_OK)

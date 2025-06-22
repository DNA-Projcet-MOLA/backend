"""
URL configuration for python_DNA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="MOLA 백엔드 API",
        default_version='v1',
        description="""MOLA (Mathematical Object Learning Assistant) 백엔드 API 문서
        
이 API는 다음과 같은 기능을 제공합니다:
- 사용자 인증 및 관리 (회원가입, 로그인, 프로필 관리)
- 수학 문제 업로드 및 관리 (이미지 OCR, 문제 분석)
- AI 기반 문제 생성

인증이 필요한 API는 헤더에 JWT 토큰을 포함해야 합니다:
Authorization: Bearer {your_access_token}
        """,
        terms_of_service="https://mola.example.com/terms/",
        contact=openapi.Contact(
            name="MOLA 개발팀",
            email="contact@mola.example.com",
            url="https://mola.example.com"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/problems/', include('problems.urls')),
    path('api/ai/', include('ai.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # User 모델의 필드를 모두 보여주고, 관리자가 쉽게 검색/수정 가능하게 확장
    fieldsets = BaseUserAdmin.fieldsets + (
        ("추가 정보", {
            'fields': (
                'real_name',
                'birthdate',
                'school',
                'student_number',
                'avatar',
            ),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("추가 정보", {
            'fields': (
                'real_name',
                'birthdate',
                'school',
                'student_number',
                'avatar',
            ),
        }),
    )
    list_display = (
        'username', 'email', 'real_name', 'birthdate',
        'school', 'student_number', 'is_staff'
    )
    search_fields = ('username', 'real_name', 'email', 'school')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
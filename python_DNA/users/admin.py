from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인정보', {'fields': ('real_name', 'birthdate', 'email', 'school', 'grade', 'classroom', 'student_number', 'avatar')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요 일자', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'real_name', 'birthdate', 'email', 'school', 'grade', 'classroom', 'student_number', 'avatar'),
        }),
    )
    list_display = ('username', 'real_name', 'email', 'school', 'grade', 'classroom', 'student_number', 'is_active', 'is_staff')
    search_fields = ('username', 'real_name', 'email', 'school')
    ordering = ('username',)

from django.contrib import admin
from .models import Problem

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'image_path', 'user', 'created_at')
    search_fields = ('question', 'user__username')
    list_filter = ('created_at', 'user')
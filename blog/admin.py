from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Админ-панель для добавления блога"""
    list_display = ('title', 'view_count')
    search_fields = ('title', 'date_publish', 'content')

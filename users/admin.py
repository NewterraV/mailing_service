from django.contrib import admin
from users.models import User, VerifyCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = 'pk', 'last_name', 'first_name', 'email', 'is_active',


@admin.register(VerifyCode)
class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = 'pk', 'verify_code', 'user'

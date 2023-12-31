from django.contrib import admin
from mailing.models import Mailing, Content, Logs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'send_today', 'owner', 'is_active')
    list_filter = ('state',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('topic',)
    search_fields = ('name', 'topic',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('last', 'status', 'response')
    list_filter = ('status',)

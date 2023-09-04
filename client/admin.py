from django.contrib import admin
from client.models import Client


@admin.register(Client)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'surname', 'email', 'comment')

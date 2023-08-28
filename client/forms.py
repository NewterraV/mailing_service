from django import forms
from mailing.forms import StyleMixin
from client.models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

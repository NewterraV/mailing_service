from django import forms
from mailing.forms import StyleMixin
from client.models import Client


class ClientForm(StyleMixin, forms.ModelForm):
    """Форма для создания получателя"""

    class Meta:
        model = Client
        exclude = 'owner',

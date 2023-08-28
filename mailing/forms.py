from django import forms
from mailing.models import Mailing, Content
from crispy_forms.helper import FormHelper
PERIOD = (
    ('day', 'День'),
    ('week', 'Месяц'),
    ('month', 'Год')
)


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class MailingForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = 'state',


class ContentForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Content
        exclude = 'settings',

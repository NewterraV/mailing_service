from django import forms
from mailing.models import Mailing, Content
from crispy_forms.helper import FormHelper
from datetime import datetime
from client.models import Client


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
        exclude = 'state', 'next_date', 'send_today', 'owner'

    def __init__(self, *args, **kwargs):
        """Переопределение для фильтрации содержимого поля clients"""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.user)

    def clean_start_date(self):
        """Метод проверяет, что введенная дата больше или равна текущей"""
        now = datetime.now().date()
        cleaned_data = self.cleaned_data.get('start_date')
        if cleaned_data < now:
            raise forms.ValidationError('Дата начала рассылки не может быть ранее текущей даты.')

        return cleaned_data

    def clean_end_date(self):
        """Метод проверяет, что введенная дата больше или равна текущей"""
        cleaned_data = self.cleaned_data.get('end_date')
        if cleaned_data < self.cleaned_data.get('start_date'):
            raise forms.ValidationError('Дата завершения рассылки не может быть ранее даты начала рассылки.')

        return cleaned_data


class ContentForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Content
        exclude = 'settings',

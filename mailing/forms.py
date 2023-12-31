from django import forms
from mailing.models import Mailing, Content, PERIOD
from crispy_forms.helper import FormHelper
from datetime import datetime
from client.models import Client


PERIOD = (
    ('day', 'День'),
    ('week', 'Месяц'),
    ('month', 'Год')
)


class StyleMixin:
    """Класс добавляющий форматирование форм crispy-forms"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class MailingForm(StyleMixin, forms.ModelForm):
    """Класс описывающий форму для создания новой рассылки"""

    class Meta:
        model = Mailing
        exclude = 'state', 'send_today', 'owner', 'next_date', 'is_active'

    def __init__(self, *args, **kwargs):
        """Переопределение для фильтрации содержимого поля clients"""

        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['clients'].queryset = Client.objects.filter(owner=self.user)

    # Возникает баг, при котором во время редатирования возникает ошибка сравнения
    # def clean_start_date(self):
    #     """Метод проверяет, что введенная дата больше или равна текущей"""
    #     now = datetime.now().date()
    #     cleaned_data = self.cleaned_data.get('start_date')
    #     if cleaned_data < now:
    #         raise forms.ValidationError('Дата начала рассылки не может быть ранее текущей даты.')
    #
    #     return cleaned_data

    def clean_end_date(self):
        """Метод проверяет, что введенная дата больше или равна текущей"""
        cleaned_data = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if cleaned_data < start_date:
            raise forms.ValidationError('Дата завершения рассылки не может быть ранее даты начала рассылки.')

        return cleaned_data


class ContentForm(StyleMixin, forms.ModelForm):
    """Класс описывающий форму для создания содержимого рассылки"""
    class Meta:
        model = Content
        exclude = 'settings',

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from mailing.forms import StyleMixin
from users.models import User, VerifyCode


class ResetPasswordForm(StyleMixin, forms.Form):

    email = forms.EmailField(label='')

    def clean_email(self):
        cleaned_data = self.cleaned_data.get('email')
        user = User.objects.filter(email=cleaned_data).first()
        if not user:
            raise forms.ValidationError('Пользователь с таким email не существует')
        return cleaned_data


class LoginForm(StyleMixin, AuthenticationForm):
    pass


class RegisterForm(StyleMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'password1', 'password2')


class UserUpdateForm(StyleMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class VerifyForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = VerifyCode
        fields = 'user_code',

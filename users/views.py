from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaselogoutView
from users.forms import LoginForm, RegisterForm, VerifyForm, UserUpdateForm, ResetPasswordForm
from users.models import User, VerifyCode
from users.services import generate_code, send_verification_mail, send_reset_password_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from users.services import block_user
from django.shortcuts import get_object_or_404


def reset_password(request):

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            new_password = User.objects.make_random_password(length=8)
            user.set_password(new_password)
            user.save()
            send_reset_password_mail(email, new_password)
            return render(request, 'users/reset_success.html')

    else:
        form = ResetPasswordForm()

    return render(request, 'users/reset_password.html', {'form': form})


@permission_required('users.block_users')
def block_user_view(request, pk):
    block_user(pk)
    return redirect(reverse('users:list_users'))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    login_url = 'users:login'
    permission_required = 'users.block_users'


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class LogoutView(BaselogoutView):
    pass


class RegisterView(CreateView):
    """Класс для отображения формы регистрации пользователя"""
    model = User
    form_class = RegisterForm

    def form_valid(self, form):
        self.object = form.save()

        group = Group.objects.get(name='user')
        self.object.groups.add(group)
        self.object.save()

        # Создаем ключ верификации пользователя и отправляем его на почту
        verify = VerifyCode.objects.create(verify_code=generate_code(), user=self.object)
        verify.save()
        send_verification_mail(self.object, verify.verify_code)
        # Редирект на страницу верификации
        return redirect(reverse('users:verify', args=[self.object.pk]))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        return self.request.user


class VerifyUpdateView(UpdateView):
    """Класс для отображения проверки кода верификации после регистрации"""
    model = VerifyCode
    form_class = VerifyForm

    def form_valid(self, form):
        self.object = form.save()

        # Сверяем код введеный пользователем
        if self.object.user_code == self.object.verify_code:
            # Меняем статус активации пользователя
            self.object.user.is_active = True
            self.object.user.save()

            # Удаляем более не требуемую запись из БД
            self.object.delete()
            return redirect(reverse('mailing:index'))

        return redirect(reverse('users:verify', args=[self.object.pk]))

from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from client.forms import ClientForm
from client.models import Client
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    """Класс отображения списка получателей"""
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }
    login_url = 'users:login'

    def get_queryset(self, *args, **kwargs):
        """Переопределение для учета типа пользователя"""
        if self.request.user.is_staff:
            queryset = super().get_queryset().all().order_by('first_name')
        else:
            queryset = super().get_queryset().filter(owner=self.request.user).order_by('first_name')
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Класс для отображения детальной информации о получателе"""
    model = Client
    extra_context = {
        'title': 'Клиент'
    }
    login_url = 'users:login'

    def get_object(self, queryset=None):
        """Переопределение для ограничения доступа к детальной информации всех кроме владельца"""
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс для отображения создания нового получателя"""
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Новый клиент'
    }
    success_url = reverse_lazy('client:list')
    login_url = 'users:login'
    permission_required = 'client.add_client'

    def form_valid(self, form):
        """Переопределение для добавления владельца записи"""
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс для отображения редактирования получателя"""
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Редактирование клиента'
    }
    login_url = 'users:login'
    permission_required = 'client.change_client'

    def get_success_url(self):
        return reverse('client:detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс для удаления получателя"""
    model = Client
    success_url = reverse_lazy('client:list')
    login_url = 'users:login'
    permission_required = 'client.delete_client'

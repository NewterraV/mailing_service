from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from client.forms import ClientForm
from client.models import Client
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }
    login_url = 'users:login'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            queryset = super().get_queryset().all().order_by('first_name')
        else:
            queryset = super().get_queryset().filter(owner=self.request.user).order_by('first_name')
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Клиент'
    }
    login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Новый клиент'
    }
    success_url = reverse_lazy('client:list')
    login_url = 'users:login'
    permission_required = 'client.add_client'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        # self.object.owner = self.request.user
        # self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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
    model = Client
    success_url = reverse_lazy('client:list')
    login_url = 'users:login'
    permission_required = 'client.delete_client'

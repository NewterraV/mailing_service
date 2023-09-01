from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from client.forms import ClientForm
from client.models import Client
from django.urls import reverse_lazy, reverse
from django.http import Http404


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().filter(owner=self.request.user).order_by('last_name')
        return queryset


class ClientDetailView(DetailView):
    model = Client
    extra_context = {
        'title': 'Клиент'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.objec


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Новый клиент'
    }
    success_url = reverse_lazy('client:list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Редактирование клиента'
    }

    def get_success_url(self):
        return reverse('client:detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')

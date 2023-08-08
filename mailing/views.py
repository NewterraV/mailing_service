from django.shortcuts import render
from mailing.models import Content, Logs
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy


def index(request):
    context = {
        'object_list': Logs.objects.all()
    }
    return render(request, 'mailing/index.html', context)


class ContentListView(ListView):
    model = Content


class ContentDetailView(DetailView):
    model = Content


class ContentCreateView(CreateView):
    model = Content
    fields = ('name', 'topic', 'content', 'last', 'status', 'response')
    success_url = reverse_lazy('mailing:mailing-list')

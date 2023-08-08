from django.shortcuts import render
from mailing.models import Content, Logs, Mailing
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy


def index(request):
    context = {
        'object_list': Logs.objects.all()
    }
    return render(request, 'mailing/index.html', context)


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Logs.objects.filter(mailing=self.kwargs['pk'])
        return context


class ContentCreateView(CreateView):
    model = Content
    fields = ('name', 'topic', 'content', 'last', 'status', 'response')
    success_url = reverse_lazy('mailing:mailing-list')

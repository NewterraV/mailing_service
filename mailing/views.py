from django.shortcuts import render
from mailing.models import Content, Logs, Mailing
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm, ContentForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from mailing.services import set_state_stopped
from client.models import Client


class MailingFormsetMixin:
    extra = 1

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        content_formset = inlineformset_factory(Mailing, Content, form=ContentForm, extra=self.extra)
        if self.request.method == 'POST':
            formset = content_formset(self.request.POST, instance=self.object)
        else:
            formset = content_formset(instance=self.object)

        context_data['formset'] = formset
        return context_data


def stopped(request, pk):
    set_state_stopped(pk)
    return redirect(reverse('mailing:mailing_list'))


def index(request):
    context = {
        'object_list': Logs.objects.all(),
        'title': 'Главная страница'
    }
    return render(request, 'mailing/index.html', context)


class LogsListView(ListView):
    model = Logs


class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.order_by('name')
        return queryset


    # def get_queryset(self, *args, **kwargs):
    #
    #     queryset = super().get_queryset(*args, **kwargs)
    #
    #     queryset = queryset.prefetch_related('content')
    #     # print(queryset.values())
    #     # # print(context)
    #     return queryset


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Logs.objects.filter(mailing=self.kwargs.get('pk'))
        context['content'] = Content.objects.filter(mailing=self.kwargs.get('pk')).first()
        context['clients'] = self.object.clients.all()
        # print(context.content.content)
        # context['title'] = f'Рассылка - {self.object.content_set.name[:20]}'
        return context


class MailingUpdateView(MailingFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    extra = 0   # переменная для ограничения форм сета

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {
        'title': 'Удаление рассылки'
    }
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(MailingFormsetMixin, CreateView):
    model = Mailing
    extra_context = {
        'title': 'Новая рассылка'
    }
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        content_formset = inlineformset_factory(Mailing, Content, form=ContentForm, extra=1)
        if self.request.method == 'POST':
            formset = content_formset(self.request.POST, instance=self.object)
        else:
            formset = content_formset(instance=self.object)

        context_data['formset'] = formset
        return context_data
    
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        
        return super().form_valid(form)

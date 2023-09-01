from django.shortcuts import render
from mailing.models import Content, Logs, Mailing
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm, ContentForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from mailing.services import set_state_stopped, set_state_mailing, send_and_log
from django.http import Http404


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


def stopped(pk):
    """Представление функции приостановки работы рассылки"""
    set_state_stopped(pk)
    return redirect(reverse('mailing:mailing_list'))


def forcibly_send(pk):
    """Представление функции приостановки работы рассылки"""
    mailing = Mailing.objects.get(pk=pk)
    send_and_log(mailing)
    return redirect(reverse('mailing:mailing', args=[pk]))


def index(request):
    """Метод представления главной страницы"""
    context = {
        'object_list': Logs.objects.all().order_by('-pk'),
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
        queryset = super().get_queryset().filter(owner=self.request.user).order_by('name')
        return queryset


class MailingDetailView(DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Logs.objects.filter(mailing=self.kwargs.get('pk')).order_by('-pk')
        context['content'] = Content.objects.filter(mailing=self.kwargs.get('pk')).first()
        context['clients'] = self.object.clients.all()
        # print(context.content.content)
        context['title'] = f'Рассылка - {self.object.name}'
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
            if self.object.next_date < self.object.start_date:
                self.object.next_date = self.object.start_date
            set_state_mailing(self.object)
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

    def get_form(self, **kwargs):
        """Метод передает авторизованного пользователя в kwargs"""
        return self.form_class(user=self.request.user)

    def get_context_data(self, *args, **kwargs):

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
            self.object.owner = self.request.user
            self.object.next_date = self.object.start_date
            set_state_mailing(self.object)
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

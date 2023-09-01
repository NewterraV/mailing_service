from django.shortcuts import render
from mailing.models import Content, Logs, Mailing
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm, ContentForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from mailing.services import set_state_stopped, set_state_mailing, send_and_log
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
    extra_context = {
        'title': 'История рассылок'
    }
    login_url = 'users:login'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            queryset = super().get_queryset().all().order_by('-pk')
        else:
            queryset = super().get_queryset().filter(mailing__owner=self.request.user).order_by('-pk')
        return queryset


class MailingListView(LoginRequiredMixin,  ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }
    login_url = 'users:login'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().filter(owner=self.request.user).order_by('name')
        if self.request.user.is_staff:
            queryset = super().get_queryset().all().order_by('name')
        else:
            queryset = super().get_queryset().filter(owner=self.request.user).order_by('name')
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
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


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MailingFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    extra_context = {
        'title': 'Редактирование рассылки'
    }

    login_url = 'users:login'
    permission_required = 'mailing.change_mailing'
    extra = 0  # переменная для ограничения форм сета


    def get_form_kwargs(self):
        """Метод передает авторизованного пользователя в kwargs"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):

        context_data = self.get_context_data()
        self.object = form.save()
        formset = context_data['formset']

        if formset.is_valid():
            self.object = form.save()
            if self.object.next_date < self.object.start_date:
                self.object.next_date = self.object.start_date
            set_state_mailing(self.object)
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.kwargs.get('pk')])


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    extra_context = {
        'title': 'Удаление рассылки'
    }
    login_url = 'users:login'
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, MailingFormsetMixin, CreateView):
    login_url = 'users:login'
    model = Mailing
    extra_context = {
        'title': 'Новая рассылка'
    }
    form_class = MailingForm
    permission_required = 'mailing.add_mailing'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self, **kwargs):
        """Метод передает авторизованного пользователя в kwargs"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    
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

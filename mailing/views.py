from django.shortcuts import render
from mailing.models import Content, Logs, Mailing
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from mailing.forms import MailingForm, ContentForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from mailing.services import set_state_stopped, set_state_mailing, send_and_log, set_is_active
from blog.models import Blog
from users.models import User
from client.models import Client
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from random import sample


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


@permission_required('mailing.stop_mailing')
def stopped(request, pk):
    """Представление функции приостановки работы рассылки"""
    if request.user.is_staff:
        raise
    set_state_stopped(pk)
    return redirect(reverse('mailing:mailing_list'))


@permission_required('mailing.disable_mailing')
def mailing_disable(request, pk):
    """Представление функции отключения рассылки"""
    set_is_active(pk)
    return redirect(reverse('mailing:mailing_list'))


@permission_required('mailing.send_mailing')
def forcibly_send(request, pk):
    """Представление функции приостановки работы рассылки"""
    mailing = Mailing.objects.get(pk=pk)
    send_and_log(mailing)
    return redirect(reverse('mailing:mailing', args=[pk]))


@login_required(login_url='users:login')
def index(request):
    """Метод представления главной страницы"""
    blogs = list(Blog.objects.all())

    if request.user.is_anonymous:
        logs = Logs.objects.all().order_by('-pk')
        mailing_count = None
        mailing_active = None
        mailing_launched = None
        clients = None
        users = None

    elif request.user.is_staff:
        logs = Logs.objects.all().order_by('-pk')
        mailing_count = Mailing.objects.all().count()
        mailing_active = Mailing.objects.filter(is_active=True).count()
        mailing_launched = Mailing.objects.filter(is_active=True, state='launched').count()
        clients = Client.objects.all().distinct('email').count()
        users = User.objects.all().count()

    else:
        logs = Logs.objects.filter(mailing__owner=request.user).order_by('-pk')
        mailing_count = Mailing.objects.filter(owner=request.user).count()
        mailing_active = Mailing.objects.filter(owner=request.user, is_active=True).count()
        mailing_launched = Mailing.objects.filter(owner=request.user, is_active=True, state='launched').count()
        clients = Client.objects.filter(owner=request.user).distinct('email').count()
        users = None

    context = {
        'logs': logs[:10],
        'logs_count': len(logs),
        'mailing_count': mailing_count,
        'mailing_active': mailing_active,
        'mailing_launched': mailing_launched,
        'blogs': sample(blogs, 3),
        'clients': clients,
        'users': users,
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

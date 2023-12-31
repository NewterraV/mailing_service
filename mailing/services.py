from mailing.models import Mailing, Logs, Content
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from django.core.mail import send_mail
from smtplib import (SMTPServerDisconnected, SMTPSenderRefused,
                     SMTPRecipientsRefused, SMTPDataError, SMTPConnectError, SMTPHeloError, SMTPNotSupportedError,
                     SMTPAuthenticationError)
from typing import Any
from users.models import User
from client.models import Client
from blog.models import Blog
from random import sample


def get_index_context(request):
    """Метод собирает контекст необходимый для домашней страницы"""

    if request.user.is_anonymous:
        logs = None
        mailing_count = None
        mailing_active = None
        mailing_launched = None
        mailing_stopped = None
        clients = None
        users = None

    elif request.user.is_staff:
        logs = Logs.objects.all().order_by('-pk')
        mailing_count = Mailing.objects.count()
        mailing_active = Mailing.objects.filter(is_active=True).count()
        mailing_stopped = Mailing.objects.filter(state='stopped').count()
        mailing_launched = Mailing.objects.filter(is_active=True, state='launched').count()
        clients = Client.objects.all().distinct('email').count()
        users = User.objects.all().count()

    else:
        logs = Logs.objects.filter(mailing__owner=request.user).order_by('-pk')
        mailing_count = Mailing.objects.filter(owner=request.user).count()
        mailing_active = Mailing.objects.filter(owner=request.user, is_active=True).count()
        mailing_stopped = Mailing.objects.filter(owner=request.user, state='stopped').count()
        mailing_launched = Mailing.objects.filter(owner=request.user, is_active=True, state='launched').count()
        clients = Client.objects.filter(owner=request.user).distinct('email').count()
        users = None

    context = {
        'logs': logs[:10] if logs else None,
        'logs_count': len(logs) if logs else None,
        'mailing_count': mailing_count,
        'mailing_active': mailing_active,
        'mailing_launched': mailing_launched,
        'mailing_stopped': mailing_stopped,
        'clients': clients,
        'users': users,
        'title': 'Главная страница'
    }
    return context


def set_state_stopped(pk: str,) -> None:
    """Метод принимает primary key и на основе него меняет атрибут state экземпляра класса Mailing"""

    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.state == 'disabled':
        return

    elif mailing.state in ['launched', 'created']:
        mailing.state = 'stopped'
        mailing.send_today = False
        mailing.save()

    elif mailing.state == 'stopped':
        mailing.state = 'created'
        set_state_mailing(mailing)
        mailing.save()


def set_is_active(pk: str,) -> None:
    """Метод переключает статус активации рассылки"""

    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = False if mailing.is_active else True
    mailing.save()



def set_state_mailings() -> None:
    """Метод перебирает рассылки, на основе текущей даты меняет статусы рассылок и
    флаги необходимости отправки рассылки в текущую дату"""

    mailings = Mailing.objects.all()
    for mailing in mailings:
        set_state_mailing(mailing)


def set_state_mailing(mailing: Any) -> None:
    """Метод принимает экземпляр рассылки. На основе текущей даты меняет статусы рассылки и
    флаг необходимости отправки рассылки в текущую дату"""
    date_now = date.today()

    if mailing.state in 'stopped':
        return

    if mailing.start_date <= date_now <= mailing.end_date:
        mailing.state = 'launched'
        check_send_day(mailing)

    elif mailing.end_date < date_now:
        mailing.state = 'completed'

    elif mailing.state == 'launched' and mailing.start_date > date_now:
        mailing.state = 'created'

    mailing.save()


def send_mailings() -> None:
    """Метод выполняет отправку почты на основе имеющихся рассылок"""
    time_now = datetime.now()

    # получение списка рассылок для отправки
    mailings = Mailing.objects.filter(send_today=True)

    for mailing in mailings:
        mailing_time = datetime.combine(date.today(), mailing.time)

        # проверка времени и создание даты следующей отправки
        if mailing_time < time_now:
            mailing.next_date = time_now + get_period(mailing.period)

            # Смена статуса рассылки на 'Завершена' в случае если дата следующей
            # отправки больше даты окончания рассылки
            if mailing.next_date.date() > mailing.end_date:
                mailing.state = 'completed'
            mailing.send_today = False
            mailing.save()
            send_and_log(mailing)


def send_and_log(mailing: Any):
    """Метод на основе экземпляра класса mailing собирает сообщение, отправляет его и создает запись в log"""
    if mailing.is_active:
        # получение контента для отправки и списка получателей
        clients = [client.email for client in mailing.clients.all()]
        content = Content.objects.filter(mailing=mailing.pk).first()

        # Отправка письма
        status = send_letter(clients, content)

        # создание лога отправки
        log = Logs.objects.create(mailing=mailing, status=status[1], response=status[0])
        log.save()
    else:
        log = Logs.objects.create(mailing=mailing, status=False, response='Рассылка была деактивирована модератором')
        log.save()


def get_period(period: str) -> Any:
    """Метод получает строковое значение периода и возвращает объект timedelta"""
    periods = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(days=7),
        'month': timedelta(days=30)
    }
    return periods[period]


def check_send_day(mailing: Any) -> None:
    """Метод проверяет, соответствует ли дата следующей отправки текущей дате, если да, то меняет send_today на True"""
    now = datetime.now().date()
    if now == mailing.next_date:
        mailing.send_today = True
        return

    mailing.send_today = False


def send_letter(recipients: list, content: Any) -> (str, bool):
    """Метод отправляет письмо и обрабатывает исключения, если они возникли при отправке.
    Возвращает кортеж (сообщение: [str], статус: [bool])"""
    try:
        send_mail(
            content.topic,
            content.content,
            settings.EMAIL_HOST_USER,
            recipients
        )
        return 'Рассылка выполнена', True

    except SMTPServerDisconnected:
        return 'Сервер неожиданно отключился', False

    except SMTPSenderRefused:
        return f'Адрес отправителя отклонен', False

    except SMTPRecipientsRefused:
        return f'Все адреса получателей отказались.', False

    except SMTPDataError:
        return f'SMTP-сервер отказался принять данные сообщения.', False

    except SMTPConnectError:
        return f'Произошла ошибка при установлении соединения с сервером..', False

    except SMTPNotSupportedError:
        return f'Использованная команда или параметр не поддерживается сервером.', False

    except SMTPAuthenticationError:
        return f'Аутентификация SMTP прошла неправильно. ', False

    except SMTPHeloError:
        return f'Сервер отклонил наше HELO сообщение.. ', False

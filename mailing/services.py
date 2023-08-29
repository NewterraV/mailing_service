from mailing.models import Mailing, Logs, Content
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from django.core.mail import send_mail
import time


def set_state_stopped(pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.state in ['launched', 'created']:
        mailing.state = 'stopped'
        mailing.save()

    elif mailing.state == 'stopped':
        mailing.state = 'created'
        mailing.save()


def set_state_mailing():
    date_now = date.today()
    mailings = Mailing.objects.all()
    for mailing in mailings:
        if mailing.state == 'stopped':
            continue

        if mailing.start_date <= date_now <= mailing.end_date:
            mailing.state = 'launched'
            mailing.save()
            print(mailing.get_state_display())

        elif mailing.end_date < date_now:
            mailing.state = 'completed'
            mailing.save()
            print(mailing.get_state_display())


def send_mailings():
    """Метод выполняет отправку почты на основе имеющихся рассылок"""
    time_now = datetime.now()
    print(time_now)

    mailings = Mailing.objects.filter(state='launched')
    for mailing in mailings:
        if mailing.last_time == time_now.date():
            mailing_time = datetime.combine(date.today(), mailing.time)
            if mailing_time < time_now:
                mailing.last_time = time_now + get_period(mailing.period)
                mailing.save()
                clients = [client.email for client in mailing.clients.all()]
                content = Content.objects.filter(mailing=mailing.pk).first()
                print(clients)
                try:
                    message = send_mail(
                        content.topic,
                        content.content,
                        settings.EMAIL_HOST_USER,
                        clients
                    )
                    status = True
                except:
                    print('1')

                print(message)
                log = Logs.objects.create(mailing=mailing, status=message, response=message)
                log.save()
                print('Успех')


def get_period(period):
    periods = {
        'hour': timedelta(hours=1),
        'day': timedelta(days=1),
        'week': timedelta(days=7),
        'month': timedelta(days=30)
    }
    return periods[period]

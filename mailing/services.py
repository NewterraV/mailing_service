from mailing.models import Mailing
from django.shortcuts import get_object_or_404


def set_state_stopped(pk):

    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.state in ['launched', 'created']:
        mailing.state = 'stopped'
        mailing.save()

    elif mailing.state == 'stopped':
        mailing.state = 'created'
        mailing.save()

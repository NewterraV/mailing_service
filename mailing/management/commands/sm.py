from django.core.management import BaseCommand
from mailing.services import send_mailings, set_state_mailings


class Command(BaseCommand):
    """Команда запускает отправку писем со статусом 'отправить сегодня'"""
    def handle(self, *args, **options):
        send_mailings()

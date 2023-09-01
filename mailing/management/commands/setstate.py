from django.core.management import BaseCommand
from mailing.services import set_state_mailings


class Command(BaseCommand):
    """Команда запускает обновление статуса всех рассылок"""
    def handle(self, *args, **options):
        set_state_mailings()

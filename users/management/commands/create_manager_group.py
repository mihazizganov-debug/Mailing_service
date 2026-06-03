from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from mailing.models import Client, Mailing

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджер" и назначает права'

    def handle(self, *args, **kwargs):
        # Создаём группу
        group, created = Group.objects.get_or_create(name='Менеджер')

        if created:
            self.stdout.write('Группа "Менеджер" создана')
        else:
            self.stdout.write('Группа "Менеджер" уже существует')

        # Права на просмотр всех клиентов
        client_ct = ContentType.objects.get_for_model(Client)
        view_client_permission = Permission.objects.get(codename='view_client', content_type=client_ct)

        # Права на просмотр всех рассылок
        mailing_ct = ContentType.objects.get_for_model(Mailing)
        view_mailing_permission = Permission.objects.get(codename='view_mailing', content_type=mailing_ct)

        group.permissions.add(view_client_permission, view_mailing_permission)

        self.stdout.write(self.style.SUCCESS('Права назначены'))

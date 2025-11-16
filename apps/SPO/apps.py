from django.apps import AppConfig
from django.core.management import call_command

class SPOConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.SPO'
    def ready(self):
        call_command('transfer_zawory')

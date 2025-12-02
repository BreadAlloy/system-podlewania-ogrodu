from django.core.management import BaseCommand
from apps.SPO.models import Wodomierz

class Command(BaseCommand):
    def handle(self, *args, **options):
        if Wodomierz.objects.filter(pk=1).exists():
            print("Wodomierz OK")
        else:
            wodomierz = Wodomierz()
            wodomierz.save()
            print("Wodomierz zrobiony OK")
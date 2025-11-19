from django.core.management import BaseCommand
import time
from apps.SPO.models import Zawor
from konfiguracja import * # możliwe, że hardware.py inaczej czyta plik konfikuracyjny, należy dbać aby tak nie było
from hardware import aktywny, nieaktywny;
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if os.environ.get('RUN_MAIN')!='true':
            print("Czytanie konfiguracji sprzetu")
            if Zawor.objects.exists():
                Zawor.objects.all().delete()
            print("Przeczytane sekcje:")
            for index, C in config.rozpiska_sekcji.items():
                name = C[0];
                z = Zawor.objects.create(real_id=index, status=nieaktywny);
                print(z);
            print("Konfiguracja sprzetu przeczytana")
from django.core.management import BaseCommand
import time
from apps.SPO.models import Zawor
from hardware import sekcje
from konfiguracja import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        #print("Started gpio-worker")
        #while True:
        print("Gpio update begin")
        Zawor.objects.all().delete()
        id_counter=0
        for _, zawor_import in sekcje.przekazniki.items():
            print(zawor_import)
            Zawor.create(real_id=id_counter, status=zawor_import.stan)
            id_counter+=1
        print("Gpio update end")
        #time.sleep(10)
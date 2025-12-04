from django.core.management import BaseCommand
from apps.SPO.models import Zawor # komunikacja przez baze danych
from konfiguracja import *
from hardware import sekcje, wodomierz, aktywny, nieaktywny
from czas import czas_globalny
from plan_podlewania import plan_podlewania, ProgramBlock, tryb_podlewania_czasem
import time # po time.sleep()
from logger import logger_globalny

class Command(BaseCommand):

    print(config.rozpiska_sekcji);
    logger_globalny.przygotuj_do_pisania();

    sekcje = sekcje();
    wodomierz = wodomierz(sekcje);

    plan = plan_podlewania()
    plan.add_free_block(ProgramBlock(czas_globalny.czas_od_epoch + 5, 2, tryb_podlewania_czasem, 10))

    def handle(self, *args, **options):
        print("Started gpio-worker")
        self.sekcje.printuj_stan();
        wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();

        for z in Zawor.objects.all():
            z.status = nieaktywny;
            z.save();

        while True:
            time.sleep(1.0/config.czestotliwosc_operowania);
            czas_globalny.update();

            self.plan.update_queue(self.wodomierz.stan_wodomierza())
            print(self.plan.aktualne_stany_sekcji())

            zawory_w_bazie = Zawor.objects.all();
            czy_cos_sie_zmienilo = False
            for z_baza in zawory_w_bazie:
                z_sprzet = self.sekcje.przekazniki[z_baza.real_id]
                if(z_baza.status != z_sprzet.stan):   # sprzet i baza inaczej nazywają to samo pole, pewnie by trzeba to poprawić
                    z_sprzet.przelacz();
                    czy_cos_sie_zmienilo = True;
            if(config.printuj_stan_przekaznikow and czy_cos_sie_zmienilo):
                self.sekcje.printuj_stan();

            if(config.symulowany_wodomierz): self.wodomierz.symulator();
            if(wczesniejszy_stan_wodomierza != self.wodomierz.stan_wodomierza()):
                self.wodomierz.zapisz_stan();
                print(f"Stan wodomierza: {self.wodomierz.stan_wodomierza()} ml");
                wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();


""" 
Jeśli np. pisze error 
TypeError: wodomierz.zapisz_stan() missing 1 required positional argument: 'self'
To najprawdopodobniej brakuje self przed wodomierz:
Poprawine: SELF.wodomierz.zapisz_stan()
"""
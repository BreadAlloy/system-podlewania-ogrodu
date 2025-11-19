from django.core.management import BaseCommand
from apps.SPO.models import Zawor # komunikacja przez baze danych
from konfiguracja import *
from hardware import sekcje, wodomierz
import time

class Command(BaseCommand):

    sekcje = sekcje();
    wodomierz = wodomierz(sekcje);

    def handle(self, *args, **options):
        print("Started gpio-worker")
        self.sekcje.printuj_stan();
        wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();

        while True:
            time.sleep(1.0/config.czestotliwosc_operowania);
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
                print(f"Stan wodomierza: {self.wodomierz.stan_wodomierza()} ml");
                wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();
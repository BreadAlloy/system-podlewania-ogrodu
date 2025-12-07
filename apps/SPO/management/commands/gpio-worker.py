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

    plan = plan_podlewania();

    sterowanie_reczne : bool = False;

    def handle(self, *args, **options):
        print("Started gpio-worker")

        from przykladowe_programy_podlewania import przykladowy_program_podlewania_1, przykladowy_program_podlewania_2, przykladowy_program_podlewania_3, przykladowy_program_podlewania_4, przykladowy_program_podlewania_5
        p1 = przykladowy_program_podlewania_1();
        p2 = przykladowy_program_podlewania_2();
        p3 = przykladowy_program_podlewania_3();
        p4 = przykladowy_program_podlewania_4();
        p5 = przykladowy_program_podlewania_5();

        self.plan.dodaj_program(p1.nazwa_programu, p1);
        self.plan.dodaj_program(p2.nazwa_programu, p2);
        self.plan.dodaj_program(p3.nazwa_programu, p3);
        self.plan.dodaj_program(p4.nazwa_programu, p4);
        self.plan.dodaj_program(p5.nazwa_programu, p5);

        self.sekcje.printuj_stan();
        wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();

        for z in Zawor.objects.all():
            z.status = nieaktywny;
            z.save();

        while True:
            time.sleep(1.0/config.czestotliwosc_operowania);
            czas_globalny.update();

            chciana_sekcja_planu = self.plan.update(self.wodomierz);

            zawory_w_bazie = Zawor.objects.all();
            czy_cos_sie_zmienilo = False;

            if(self.sterowanie_reczne):
                for z_baza in zawory_w_bazie:
                    z_sprzet = self.sekcje.przekazniki[z_baza.real_id]
                    if(z_baza.status != z_sprzet.stan):   # sprzet i baza inaczej nazywają to samo pole, pewnie by trzeba to poprawić
                        z_sprzet.przelacz();
                        czy_cos_sie_zmienilo = True;
            else:
                for index, zawor in self.sekcje.przekazniki.items():
                    if(chciana_sekcja_planu is not None and index == chciana_sekcja_planu):
                        if(zawor.stan == nieaktywny):
                            zawor.przelacz();
                            czy_cos_sie_zmienilo = True;
                    else:
                        if(zawor.stan == aktywny):
                            zawor.przelacz();
                            czy_cos_sie_zmienilo = True;
                    zawory_w_bazie[index].status = zawor.stan;

            if(config.printuj_stan_przekaznikow and czy_cos_sie_zmienilo):
                self.sekcje.printuj_stan();

            if(config.symulowany_wodomierz): self.wodomierz.symulator();
            if(wczesniejszy_stan_wodomierza != self.wodomierz.stan_wodomierza()):
                self.wodomierz.zapisz_stan();
                # print(f"Stan wodomierza: {self.wodomierz.stan_wodomierza()} ml");
                wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();


""" 
Jeśli np. pisze error 
TypeError: wodomierz.zapisz_stan() missing 1 required positional argument: 'self'
To najprawdopodobniej brakuje self przed wodomierz:
Poprawine: SELF.wodomierz.zapisz_stan()
"""
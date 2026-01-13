from django.core.management import BaseCommand
from apps.SPO.models import Zawor # komunikacja przez baze danych
from konfiguracja import *
from hardware import sekcje, wodomierz, aktywny, nieaktywny
from czas import czas_globalny
from plan_podlewania import plan_podlewania, ProgramBlock, tryb_podlewania_czasem
import time # po time.sleep()
from logger import logger_globalny
from komunikator import *

class Command(BaseCommand):

    print(config.rozpiska_sekcji);

    sekcje = sekcje();
    wodomierz = wodomierz(sekcje);

    plan = plan_podlewania();

    sterowanie_reczne : bool = False;

    def handle(self, *args, **options):
        print("Started gpio-worker")
        
        self.sekcje.printuj_stan();
        wczesniejszy_stan_wodomierza = self.wodomierz.stan_wodomierza();

        self.plan.przeczytaj_programy_z_pliku();

        for p in self.plan.programy.values():
            print(p);

        for z in Zawor.objects.all():
            z.status = nieaktywny;
            z.save();

        discord = None;
        while True:
            
            odebrane = None;
            if(discord != None):
                try:
                    odebrane = discord.odbierz();
                except EOFError:
                    print("Polaczenie z web zerwane");
                    discord = None;
                    continue;
            else:
                print("Czekam na polaczenie z web");
                discord = komunikator('gpio-worker', config.port_do_komunikacji);
                discord.serwuj();
                print("Jest polaczenie z web :)");


            time.sleep(1.0/config.czestotliwosc_operowania);
            czas_globalny.update();

            czy_cos_sie_zmienilo = False;



            if(odebrane is not None):
                if  (odebrane[0].kod == kody_komunikatow.USUN_PROGRAM):
                    self.plan.usun_program(odebrane[1]);

                elif(odebrane[0].kod == kody_komunikatow.ZMODYFIKUJ_PROGRAM):
                    #self.plan.zmodyfikuj_program(odebrane[1].nazwa_programu,odebrane[1]);
                    self.plan.zmodyfikuj_program(odebrane[1]);

                elif(odebrane[0].kod == kody_komunikatow.DODAJ_PROGRAM):
                    #self.plan.dodaj_program(odebrane[1].nazwa_programu,odebrane[1]);
                    self.plan.dodaj_program(odebrane[1]);

                else:
                    print("Cos tu nie tak");

            if(self.sterowanie_reczne):
                zawory_w_bazie = Zawor.objects.all();
                for z_baza in zawory_w_bazie:
                    z_sprzet = self.sekcje.przekazniki[z_baza.real_id]
                    if(z_baza.status != z_sprzet.stan):   # sprzet i baza inaczej nazywają to samo pole, pewnie by trzeba to poprawić
                        z_sprzet.przelacz();
                        czy_cos_sie_zmienilo = True;
            else:
                chciana_sekcja_planu = self.plan.update(self.wodomierz);

                for index, zawor in self.sekcje.przekazniki.items():
                    if(chciana_sekcja_planu is not None and index == chciana_sekcja_planu):
                        if(zawor.stan == nieaktywny):
                            zawor.przelacz();
                            czy_cos_sie_zmienilo = True;
                    else:
                        if(zawor.stan == aktywny):
                            zawor.przelacz();
                            czy_cos_sie_zmienilo = True;

                # Z jakiegoś nieznanego mi powodu
                #   zawory_w_bazie = Zawor.objects.order_by("real_id");
                #   zawory_w_bazie[index].status = zawor.stan;
                # Nie działa

                for z in Zawor.objects.all():
                    if(z.status != self.sekcje.przekazniki[z.real_id].stan):
                        z.status = self.sekcje.przekazniki[z.real_id].stan;
                        z.save();

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
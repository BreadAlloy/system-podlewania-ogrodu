
from konfiguracja import *
import time
import random
import math

# jest tak bo diody indykatorowe tak mam na płytce z przekaźnikami i raspberry taki stan ma defaultowo
aktywny = True;
nieaktywny = False;

class przekaznik:
    stan : bool = nieaktywny;
    pin = None;

    def __init__(self, pin_number : int):
        if(not config.debug_poza_raspberry):
            from gpiozero import LED # pip install gpiozero, lgpio, pigpio
            self.pin = LED(pin_number);
            # wyłącz sekcje. Tak jest to dziwne jak ktoś ma pomysł jak to zrobić czytelniej to proszę o podpowiedź
            self.pin.on();

    def aktywuj(self):
        assert(self.stan == nieaktywny);
        if(not config.debug_poza_raspberry): self.pin.off(); # włącz sekcje
        self.stan = aktywny;

    def deaktywuj(self):
        assert(self.stan == aktywny);
        if(not config.debug_poza_raspberry): self.pin.on(); # wyłącz sekcje
        self.stan = nieaktywny;

    def przelacz(self):
        """ Raczej nie powinno być używane poza debugiem z powodów bezpieczeństwa programu"""
        if(self.stan == aktywny):
            self.deaktywuj();
        else:
            self.aktywuj();

    def stan_str(self) -> str:
        if(self.stan == aktywny):
            return "aktywny";
        else: 
            return "nieaktywny";

    def __str__(self):
        return f"przekaznik: {self.stan_str()}\n";

class sekcje: # singleton
    # id_sekcji : przekaznik
    przekazniki = {};
    
    def __init__(self):
        for numer_sekcji, C in config.rozpiska_sekcji.items():
            GPIOpin = C[1];
            self.przekazniki[numer_sekcji] = przekaznik(GPIOpin);

    def printuj_stan(self):
        """ Printowanie działa ale nie ma inputu z konsoli wraz z nim"""

        # print("\033[A\033[A\033[A\r", end = "");  #cofanie o 3 linijki
        for _, zawor in self.przekazniki.items():
            if(zawor.stan == aktywny):
                print("\033[42m  ", end = "");
            else:
                print("\033[41m  ", end = "");
            print("\033[47m|", end = "");
        print("\033[40m\n", end = "");
        # print("\033[40m\n\n\n", end = "");  #przewiniecie z powrotem do przodu o 3 linijki

class wodomierz: # singleton
    miernik = None;
    liczba_sygnalow : int = 0;
    sekcje_ptr = None; # musi znać stan sekcji aby symulować wylewanie wody gdy któraś sekcja jest aktywna
    miernik_czasu = time.time();

    def __init__(self, sekcje_ptr):
        if(not config.symulowany_wodomierz):
            from gpiozero import Button # pip install gpiozero, lgpio, pigpio
            self.miernik = Button(config.pin_do_wodomierza);
            self.miernik.when_pressed = lambda: self.sygnal();
        self.sekcje_ptr = sekcje_ptr;

    def stan_wodomierza(self):
        return float(self.liczba_sygnalow) * config.ilosc_wody_na_sygnal;

    def sygnal(self):
        # print(f"Stan wodomierza: {self.stan_wodomierza()} ml");
        self.liczba_sygnalow+=1;

    def symulator(self):
        nowy_czas = time.time();
        ile_uplynelo = nowy_czas - self.miernik_czasu;
        self.miernik_czasu = nowy_czas;

        ile_jest_aktywnych = 0;
        for _, z in self.sekcje_ptr.przekazniki.items():
            if(z.stan == aktywny): ile_jest_aktywnych += 1;

        ile_sygnalow_sie_nalezy = 0;
        if(ile_jest_aktywnych != 0):
            ile_sygnalow_sie_nalezy = ((config.symulowana_ilosc_wylewana / config.ilosc_wody_na_sygnal) * ile_uplynelo) * (2.0 * (-1.0/float(ile_jest_aktywnych) + 1.0) + 1.0);

        ile_calych = math.floor(ile_sygnalow_sie_nalezy);
        for i in range(0, ile_calych):
            self.sygnal();
        if(random.uniform(0.0, 1.0) < (ile_sygnalow_sie_nalezy - ile_calych)):
            return self.sygnal();

    
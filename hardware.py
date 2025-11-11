
from konfiguracja import *

# jest tak bo diody indykatorowe tak mam na płytce z przekaźnikami i raspberry taki stan ma defaultowo
aktywny = True;
nieaktywny = False;

class przekaznik:
    stan : bool = nieaktywny;
    pin = None;

    def __init__(self, pin_number : int):
        if(not config.debug_poza_raspberry):
            from gpiozero import LED # pip install gpiozero, lgpio, pigpio, rpigpio
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

class sekcje:
    przekazniki = {};
    
    def __init__(self):
        for numer_sekcji, GPIOpin in config.rozpiska_sekcji.items():
            self.przekazniki[numer_sekcji] = przekaznik(GPIOpin);

    def printuj_stan(self):
        """ Printowanie działa ale nie ma inputu z konsoli wraz z nim"""

        print("\033[A\033[A\033[A\r", end = "");
        for _, zawor in self.przekazniki.items():
            if(zawor.stan == aktywny):
                print("\033[42m  ", end = "");
            else:
                print("\033[41m  ", end = "");
            print("\033[47m|", end = "");
        print("\033[47m\n\n\n", end = "");


    
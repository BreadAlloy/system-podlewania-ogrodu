from hardware import sekcje, wodomierz
from konfiguracja import *
from time import sleep

if __name__ == '__main__':
    print("Testowanie");

    print(config.rozpiska_sekcji);
    sekcje = sekcje();
    wodomierz = wodomierz(sekcje);
    
    print(sekcje.przekazniki);
    while(True):
        for _, zawor in sekcje.przekazniki.items():
            sekcje.printuj_stan();
            sleep(1.0/config.czestotliwosc_operowania);
            zawor.aktywuj();
            sekcje.printuj_stan();
            sleep(1.0/config.czestotliwosc_operowania);
            zawor.deaktywuj();
            sekcje.printuj_stan();
            sleep(1.0/config.czestotliwosc_operowania);
            zawor.przelacz();
            sekcje.printuj_stan();
            sleep(1.0/config.czestotliwosc_operowania);
            zawor.przelacz();
            if(config.symulowany_wodomierz): wodomierz.symulator();
            print(f"Stan wodomierza: {wodomierz.stan_wodomierza()} ml");


from hardware import sekcje
from konfiguracja import *
from time import sleep

if __name__ == '__main__':
    print("Testowanie");

    print(config.rozpiska_sekcji);
    sekcje = sekcje();

    print(sekcje.przekazniki);
    while(True):
        for _, zawor in sekcje.przekazniki.items():
            sekcje.printuj_stan();
            sleep(0.05);
            zawor.aktywuj();
            sekcje.printuj_stan();
            sleep(0.05);
            zawor.deaktywuj();
            sekcje.printuj_stan();
            sleep(0.05);
            zawor.przelacz();
            sekcje.printuj_stan();
            sleep(0.05);
            zawor.przelacz();



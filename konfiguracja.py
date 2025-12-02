"""
Tu się tylko czyta w trakcie działania programu
Prosze nie pushujcie go na repo jak nic nie dodaliście
"""

import os

class konfiguracja:
    debug_poza_raspberry : bool;
    printuj_stan_przekaznikow : bool = False;

    pin_do_wodomierza = 26;
    ilosc_wody_na_sygnal = 35.0; # ml/1, nie znam prawdziwej ilosci po prostu jakaś liczba
    
    symulowany_wodomierz : bool = False;
    symulowana_ilosc_wylewana = 155.0; # ml/s * aktywna_sekcja

    avg_litry_na_minute = 60.0;

    czas_przyspieszony : bool = False;       # jak się używa to zapewne należy czestotliwość operowania zwiększyć
    ile_przyspieszenia_na_update : int = 59; # sekundy | jak o za dużo na raz będzie zwiększać to może nie działać jakaś logika w programie. 59 powinno być bezpieczne.

    czestotliwosc_operowania = 1.0; # hz | nie uwzglednia czasu pracy jednego odswiezenia;

    # w normalnym uzytkowaniu nie będzie się używać "dodatkowa n" tylko po prostu się nie wpisze
    rozpiska_sekcji = {
# id_sekcji  :  (nazwa, numer_gpio)
        0 : ("Nowe drzewa", 25),
        1 : ("Rabatki kolo domu", 11),
        2 : ("Rabatka gorka", 23),
        3 : ("Trawnik kolo domu: kasztan, kuchnia", 5),
        4 : ("Trawnik kolo domu: przed domem", 18),
        5 : ("Trawnik kolo domu: judaszowniec, magnolia", 6),
        6 : ("Trawnik daleko od domu: kolo szopki", 12),
        7 : ("Trawnik daleko od domu: dołek", 13),
        8 : ("Trawnik daleko od domu: las judaszowcowy", 16),
        9 : ("Trawnik daleko od domu: duże drzewa przy drodze", 20),
       10 : ("dodatkowa 1", 10),
       11 : ("dodatkowa 2", 24),
       12 : ("dodatkowa 3", 9),
       13 : ("dodatkowa 4", 19),
       14 : ("dodatkowa 5", 21)
    };

    def __init__(self):
        RPI = os.environ.get("RPI");
        if(RPI == "false" or RPI == "False"):
            self.debug_poza_raspberry = True;
        elif(RPI == "True" or RPI == "true" or RPI == "" or RPI == None):
            self.debug_poza_raspberry = True;
        else:
            print(f"Nie wiadomo co zrobic ze zmienna srodowiskowa RPI({RPI})");
            assert(False);
        print(f"Debug poza raspberry: {self.debug_poza_raspberry}");

        #zależności w configu
        self.symulowany_wodomierz = self.symulowany_wodomierz or self.debug_poza_raspberry;
        self.printuj_stan_przekaznikow = self.printuj_stan_przekaznikow or self.debug_poza_raspberry;

config = konfiguracja();
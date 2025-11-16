"""
Tu się tylko czyta w trakcie działania programu
Prosze nie pushujcie go na repo jak nic nie dodaliście
"""

class konfiguracja:
    debug_poza_raspberry = False;
    # Printowanie działa ale nie ma inputu z konsoli wraz z nim i czyni console brzydką
    printuj_stan_przekaznikow = True or debug_poza_raspberry;

    pin_do_wodomierza = 26;
    ilosc_wody_na_sygnal = 35; # ml/1, nie znam prawdziwej ilosci po prostu jakaś liczba
    
    symulowany_wodomierz = False or debug_poza_raspberry;
    symulowana_ilosc_wylewana = 155; # ml/s

    czestotliwosc_operowania = 1.0; # hz | nie uwzglednia czasu pracy jednego odswiezenia;

    # w normalnym uzytkowaniu nie będzie się używać "dodatkowa n" tylko po prostu się nie wpisze
    rozpiska_sekcji = {
# id_sekcji  :  (nazwa, numer_gpio)
        0 : ("dodatkowa 1", 10),
        1 : ("dodatkowa 2", 24),
        2 : ("dodatkowa 3", 9),
        3 : ("Nowe drzewa", 25),
        4 : ("Rabatki kolo domu", 11),
        5 : ("Rabatka gorka", 23),
        6 : ("Trawnik kolo domu: kasztan, kuchnia", 5),
        7 : ("Trawnik kolo domu: przed domem", 18),
        8 : ("Trawnik kolo domu: judaszowniec, magnolia", 6),
        9 : ("Trawnik daleko od domu: kolo szopki", 12),
       10 : ("Trawnik daleko od domu: dołek", 13),
       11 : ("Trawnik daleko od domu: las judaszowcowy", 16),
       12 : ("Trawnik daleko od domu: duże drzewa przy drodze", 20),
       13 : ("dodatkowa 4", 19),
       14 : ("dodatkowa 5", 21)
    };

config = konfiguracja();
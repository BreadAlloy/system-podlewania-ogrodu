"""
Tu się tylko czyta w trakcie działania programu
Prosze nie pushujcie go na repo jak nic nie dodaliście
"""

class konfiguracja:
    debug_poza_raspberry = False;
    # Printowanie działa ale nie ma inputu z konsoli wraz z nim i czyni console brzydką
    printuj_stan_przekaznikow = False or debug_poza_raspberry;

    rozpiska_sekcji = {
# sekcja  :  numer_GPIO
        0 : 10,
        1 : 24,
        2 : 9,
        3 : 25,
        4 : 11,
        5 : 23,
        6 : 5,
        7 : 18,
        8 : 6,
        9 : 12,
       10 : 13,
       11 : 16,
       12 : 20,
       13 : 19,
       14 : 21
    };

config = konfiguracja();
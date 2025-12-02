import time
from konfiguracja import config

# program operuje z dokładnoscią do minut

class czas_przyspieszalny:
    czas_od_epoch : int = time.time();  # sekundy
    czas_stempel : time = time.localtime(czas_od_epoch);

    def update(self):
        if(config.czas_przyspieszony):
            self.czas_od_epoch += config.ile_przyspieszenia_na_update;
        else:
            self.czas_od_epoch  = time.time();
        self.czas_stempel = time.localtime(self.czas_od_epoch);

    def ladny_str(self):
        CS = self.czas_stempel; 
        return f"{CS.tm_hour:02}:{CS.tm_min:02}:{CS.tm_sec:02} | {CS.tm_mday:02}/{CS.tm_mon:02}/{CS.tm_year}";

    def __str__(self):
        return str(self.czas_stempel); # ma pola niepokazywane w ladny_str()

    def get_weekday(self):
        return self.czas_stempel.tm_wday

czas_globalny = czas_przyspieszalny();

class zegarek:
    godzina : int;
    minuta : int;

    def __init__(self, godzina, minuta):
        assert(godzina >= 0 and godzina < 24);
        assert(minuta >= 0 and minuta < 60);
        self.godzina = godzina;
        self.minuta = minuta;

    def __str__(self):
        return f"{self.godzina:02}:{self.minuta:02}";
import time
from konfiguracja import config

# program operuje z dokładnoscią do minut

sekundy_w_dniu = 60 * 60 * 24;

class czas_przyspieszalny:
    czas_od_epoch : int = time.time();  # sekundy
    czas_stempel : time = time.localtime(czas_od_epoch);

    def __init__(self, czas_od_epoch : int):
        self.czas_od_epoch = czas_od_epoch;
        self.czas_stempel = time.localtime(self.czas_od_epoch);

    def copy(self):
        return czas_przyspieszalny(self.czas_od_epoch);

    def update(self):
        if(config.czas_przyspieszony):
            self.czas_od_epoch += config.ile_przyspieszenia_na_update;
        else:
            self.czas_od_epoch  = time.time();
        self.czas_stempel = time.localtime(self.czas_od_epoch);

    def dodaj_czas(self, sekundy : int):
        self.czas_od_epoch += sekundy;
        self.czas_stempel = time.localtime(self.czas_od_epoch);

    def ladny_str(self):
        CS = self.czas_stempel; 
        return f"{CS.tm_hour:02}:{CS.tm_min:02}:{CS.tm_sec:02} | {CS.tm_mday:02}/{CS.tm_mon:02}/{CS.tm_year}";

    def __str__(self):
        return str(self.czas_stempel); # ma pola niepokazywane w ladny_str()

    def get_weekday(self):
        return self.czas_stempel.tm_wday
    
    def get_godzina(self):
        return self.czas_stempel.tm_hour, self.czas_stempel.tm_min

    def __lt__(self, drugi):
        return self.czas_od_epoch < drugi.czas_od_epoch;

czas_globalny = czas_przyspieszalny(time.time());

class zegarek:
    godzina : int;
    minuta : int;

    def __init__(self, godzina: int = 0, minuta: int = 0):
        assert(godzina >= 0 and godzina < 24);
        assert(minuta >= 0 and minuta < 60);
        self.godzina = godzina;
        self.minuta = minuta;

    def __str__(self):
        return f"{self.godzina:02}:{self.minuta:02}";

    def in_minutes(self) -> int:
        return self.godzina * 60 + self.minuta
    
    def from_timestamp(self, timestamp):
        self.godzina = time.localtime(timestamp).tm_hour
        self.minuta = time.localtime(timestamp).tm_min
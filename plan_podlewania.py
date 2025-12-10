from konfiguracja import config
from czas import zegarek, czas_globalny, czas_przyspieszalny, sekundy_w_dniu
import time
from logger import logger_globalny, Waznosc
import heapq
from hardware import wodomierz

# w c++ były by to constexpry
tryb_podlewania_czasem = True;
tryb_podlewania_iloscia = False;

# {timestamp: int, sekcje: int, tryb: bool, z_programu : program_podlewania, ilosc: sekundy|ml}
class ProgramBlock:
    def __init__(self, start_czas_od_epoch: int, sekcja: int, tryb: bool, z_programu, ilosc: float = 0.0):
        self.czas_wykonania = czas_przyspieszalny(start_czas_od_epoch);
        self.sekcja = sekcja
        self.tryb = tryb
        self.ilosc = ilosc; # sekundy albo ml;
        self.program = z_programu;   # z programu nie moge typehintować bo program_podlewana nie jest jeszcze zdefiniowane

    def __str__(self):
        return f"start: {self.czas_wykonania.ladny_str()} sekcja: {self.sekcja} tryb {self.tryb} ilosc: {self.ilosc}"

    def __repr__(self):   # bo print(list) tego używa
        return self.__str__();

    def copy(self):
        return ProgramBlock(self.czas_wykonania.czas_od_epoch, self.sekcja, self.tryb, self.program, self.ilosc);

    # gdy blok jest przekazywany do wykonania to generowany jest blok do następnej aktywacji
    # na podstawie programu z którego pochodzi.
    def wygeneruj_kolejny(self):
        nowy = self.copy();

        # znajdź dzień w którym dozwolone jest wykonanie podlewania
        for i in range(0, 7):
            nowy.czas_wykonania.dodaj_czas(nowy.program.co_ile_dni_podlac * sekundy_w_dniu);
            if(nowy.program.w_ktore_dni_tygodnia_podlewac[nowy.czas_wykonania.get_weekday()]):
                return nowy;

        nowy.ilosc = 0.0;
        logger.log("Nie znaleziono czasu dla ProgramBloku, zwracam z iloscia 0.0", Waznosc.KRYTYCZNE);
        return nowy;

    # do sortowania w kolejce na podstawie czasu wykonania
    def __lt__(self, drugi):
        return self.czas_wykonania < drugi.czas_wykonania;


# informacje kontrolne używane podczas wykonywania ProgramBloku
class StateofProgramBlock:
    def __init__(self, block: ProgramBlock):
        self.program_block = block
        self.wylal_wody = 0.0;
        self.sekundy_trwania = 0.0;
        self.stan = True;
        logger_globalny.log(f"Rozpoczeto podlewanie na sekcji: {self.program_block.sekcja}");

    # plan dodaje delte wykorzystanych zasobów z każdym odświeżeniem
    def add_delta(self, delta_wody: float, delta_czasu: float):
        self.wylal_wody += delta_wody;
        self.sekundy_trwania += delta_czasu;

    # sprawdza czy jest już pora zakończyć, zwrócenie False oznacza, że należy zamknąć jego sekcje.
    def update_state(self):
        if(self.program_block.tryb == tryb_podlewania_czasem):
            if(self.sekundy_trwania > self.program_block.ilosc):
                self.stan = False;
        else:
            if(self.wylal_wody > self.program_block.ilosc):
                self.stan = False;
        if(self.stan == False):
            logger_globalny.log(f"Zakonczono podlewanie po: {self.sekundy_trwania} sekundach i {self.wylal_wody} ml wylanej wody", Waznosc.INFO);
        return self.stan;

    def get_state(self) -> bool:
        return self.stan

class program_podlewana:
#---------------------------------POLA------------------------------------
    nazwa_programu : str; # aby było przyjemnie

    godzina_rozpoczecia : zegarek;

    tryb_podlewania : bool;

    #                              index 0 to poniedziałek, 1 to wtorek, itd.
    w_ktore_dni_tygodnia_podlewac : list[bool];

    # kolejność na liście to też jest kolejność uruchamiania.
    # raczej każda sekcja powinna być na liście tylko, może być podlewana przez 0 czasu
    #                       id_sekcji, czas_podlewania(min, litry)
    ilosci_podlewania : list[list[int, float]];

    co_ile_dni_podlac : int; # raczej mniejsze od 5, nie wiem co 0 oznacza

#---------------------------------POLA------------------------------------

    def __init__(self):
        """ Inicjalizuje program podlewania na działające ustawienia, a potem użytkownik sobie w webapp zmienia"""

        self.nazwa_programu = "PROGRAM PODLEWANIA";

        # defaultowo podlewa o północy
        self.godzina_rozpoczecia = zegarek(00, 00);

        # defaultowo podlewa na podstawie czasu
        self.tryb_podlewania = tryb_podlewania_czasem;

        # defaultowo podlewa w każdy dzień tygodnia
        self.w_ktore_dni_tygodnia_podlewac = [True, True, True, True, True, True, True];

        # czyta sekcje z configu i defaultowo daje 0.0 min podlewania dla każdej
        # webapp należy wyświetlić nazwe sekcji nie jej id
        self.ilosci_podlewania = [];
        for id_sekcji, _ in config.rozpiska_sekcji.items():
            self.ilosci_podlewania.append([id_sekcji, 0.0]);

        #defaultowo codziennie podlewa
        self.co_ile_dni_podlac = 1;

    def zmodyfikuj_ilosc(self, id_sekcji : int, nowa_ilosc = float) -> None:
        for i in range(0, len(self.ilosci_podlewania)):
            if(self.ilosci_podlewania[i][0] == id_sekcji):
                self.ilosci_podlewania[i][1] = nowa_ilosc;
                return None;
        assert(False); # Nie ma sekcji o takim id

    # funkcja pomocnicza do ładnego printowania
    def tryb_str(self) -> str:
        if(self.tryb_podlewania == tryb_podlewania_czasem):
            return "tryb podlewania czasem";
        return "tryb podlewania iloscia wylanej wody";
    
    def __str__(self) -> str:
        def rozpiska_dla_sekcji(self) -> str:
            ret = "id_sekcji : ilość\n";
            jednostka = "";
            if(self.tryb_podlewania == tryb_podlewania_czasem):
                jednostka = "min";
            else:
                jednostka = "litry";

            for id_sekcji, ilosc in self.ilosci_podlewania:
                ret += f"{id_sekcji}: {ilosc} {jednostka}\n";
            return ret;

        return f"""
    ---=== {self.nazwa_programu} ===---
godzina rozpoczecia: {self.godzina_rozpoczecia},
tryb podlewania: {self.tryb_str()} 
dozwolone dni do podlewania:
poniedziałek: {self.w_ktore_dni_tygodnia_podlewac[0]},
wtorek: {self.w_ktore_dni_tygodnia_podlewac[1]},
środa: {self.w_ktore_dni_tygodnia_podlewac[2]},
czwartek: {self.w_ktore_dni_tygodnia_podlewac[3]},
piątek: {self.w_ktore_dni_tygodnia_podlewac[4]},
sobota: {self.w_ktore_dni_tygodnia_podlewac[5]},
niedziela: {self.w_ktore_dni_tygodnia_podlewac[6]},
Rozpiska dla sekcji:
{rozpiska_dla_sekcji(self)}\
co ile dni podlewać: {self.co_ile_dni_podlac}        
"""

    # w miejscu zmienia trym podlewania z poprawną zaminą jednostek ilości
    def przelacz_tryb_podlewania(self) -> None:
        for i in self.ilosci_podlewania:
            if(self.tryb_podlewania == tryb_podlewania_czasem):
                i[1] = i[1] * config.avg_litry_na_minute;
            else:
                i[1] = i[1] / config.avg_litry_na_minute;
        self.tryb_podlewania = not self.tryb_podlewania;

    def czy_poprawny() -> bool:
        return False;

    # używa się tylko po dodniu programu do planu, albo przy inicjalizacji
    def daj_ProgramBlocki(self) -> list[ProgramBlock]:
        czas_rozpoczecia = czas_globalny.copy();
        # znajdź nastepny możliwy czas aktywacji

        _, cur_minuta = czas_rozpoczecia.get_godzina();
        #   0   1    2    3    4   .........    57     58    59    |   diff
        #           cur                        rozp                |    55
        #                rozp                          cur         |    5
        #      formuła:      (rozp - cur) % 60
        diff_minuty = (self.godzina_rozpoczecia.minuta - cur_minuta) % 60;
        czas_rozpoczecia.dodaj_czas(diff_minuty * 60);

        cur_godzina, _ = czas_rozpoczecia.get_godzina();
        #   0   1    2    3    4   .........    21     22    23    |   diff
        #      cur                                    rozp         |    21
        #                rozp                   cur                |    6
        #      formuła :     (rozp - cur) % 24
        diff_godzina = (self.godzina_rozpoczecia.godzina - cur_godzina) % 24;
        czas_rozpoczecia.dodaj_czas(diff_godzina * 60 * 60);

        # znajdź dzień w którym dozwolone jest wykonanie podlewania
        for i in range(0, 8):
            if(self.w_ktore_dni_tygodnia_podlewac[czas_rozpoczecia.get_weekday()]):
                break;
            if(i == 7):
                logger_globalny.log(f"Program: {self.nazwa_programu} nie znalazl czasu do startu", Waznosc.KRYTYCZNE)
                return [];
            czas_rozpoczecia.dodaj_czas(sekundy_w_dniu * self.co_ile_dni_podlac);

        # ProgramBlock używa innych jednostek, trzeba zamienić
        mnoznik_jednostek = 1;
        if(self.tryb_podlewania == tryb_podlewania_czasem):
            mnoznik_jednostek *= 60;  # 60 sekund w minucie
        else:
            mnoznik_jednostek *= 1000; # 1000 ml w litrze

        bloki = [];
        for sekcja, ilosc in self.ilosci_podlewania:
            bloki.append(ProgramBlock(czas_rozpoczecia.czas_od_epoch, sekcja, self.tryb_podlewania, self, ilosc * mnoznik_jednostek));
            if(self.tryb_podlewania == tryb_podlewania_czasem):
                czas_rozpoczecia.dodaj_czas(ilosc * 60);
            else:
                czas_rozpoczecia.dodaj_czas((ilosc / config.avg_litry_na_minute) * 60);

        return bloki;


class plan_podlewania:
#---------------------------------POLA------------------------------------

    #           {nazwa_programu : program}
    programy : dict[str, program_podlewana] = {};
    # !!!!!! ZAKAZ MODYFIKOWANIA PÓL W PROGRAMACH PODLEWANIA TUTAJ !!!!!!!

    wykonywane_ProgramBloki : list[StateofProgramBlock];  # kolejka po momencie dodania do listy
    przyszle_ProgramBloki : list[ProgramBlock];

#---------------------------------POLA------------------------------------

    def __init__(self):
        self.last_check_time = czas_globalny.czas_od_epoch
        self.last_stan_wodomierza = 0
        self.przyszle_ProgramBloki = [];
        self.wykonywane_ProgramBloki = []; # przeważnie tu powinien być jeden obiekt ale w wypadku kolizji mogą być kilka

    def zmodyfikuj_program(self, nazwa_programu : str, nowy_program):
        # usuwa wszystkie małe(te robione w kalendarzu, jednorazowe) modyfikacje dla danego programu
        nowy_program.czy_poprawny();
        pass

    # dodaj program i zintegruj jego bloku z pozostałymi
    def dodaj_program(self, nazwa_programu: str, nowy_program: program_podlewana): # Nie jestem pewnien czy dodać defaultowy program i potem go modyfikować czy podać jako argument nowy program
        self.programy[nazwa_programu] = nowy_program;
        nowe_bloki = nowy_program.daj_ProgramBlocki();
        for blok in nowe_bloki:
            heapq.heappush(self.przyszle_ProgramBloki, blok);

    # zwraca sekcje która ma być aktywna, albo None jeśli wszystkie mają być wyłączone
    def update(self, wodamierz : wodomierz) -> int|None:
        czas_diff = czas_globalny.czas_od_epoch - self.last_check_time;
        self.last_check_time = czas_globalny.czas_od_epoch;

        woda_diff = wodomierz.stan_wodomierza(wodamierz) - self.last_stan_wodomierza;
        self.last_stan_wodomierza = wodomierz.stan_wodomierza(wodamierz);

        if(len(self.przyszle_ProgramBloki) != 0):
            # które bloki należy zacząć wykonywać teraz, przekaż je do odpowiedniej kolejki
            while(self.przyszle_ProgramBloki[0].czas_wykonania < czas_globalny):
                do_wykonania = heapq.heappop(self.przyszle_ProgramBloki);
                
                # dla każdego usuwanego bloku dodaj jego następne użycie
                nowy = do_wykonania.wygeneruj_kolejny();
                heapq.heappush(self.przyszle_ProgramBloki, nowy);

                if(do_wykonania.ilosc != 0.0):  # nie ma co wykonywać pustech bloków, chociaż logika powinna być na nie odporna, ale logi wtedy są brzydkie
                    self.wykonywane_ProgramBloki.append(StateofProgramBlock(do_wykonania));
        else:
            pass
            #nie ma programów?!?!?
    
        # który ProgramBlok chce być wykonawany?
        if(len(self.wykonywane_ProgramBloki) != 0):
            blok_aktywny = self.wykonywane_ProgramBloki[0];
            blok_aktywny.add_delta(woda_diff, czas_diff);
            
            # czy należy skończyć aktywny blok ?
            while(len(self.wykonywane_ProgramBloki) != 0 and not self.wykonywane_ProgramBloki[0].update_state()):
                self.wykonywane_ProgramBloki.pop(0);

            # ta sekcja ma się dalej wykonywać
            if(len(self.wykonywane_ProgramBloki) != 0):
                return self.wykonywane_ProgramBloki[0].program_block.sekcja;
        else:
            return None;

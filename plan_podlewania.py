from konfiguracja import config
from czas import zegarek, czas_globalny

# w c++ były by to constexpry
tryb_podlewania_czasem = True;
tryb_podlewania_iloscia = False;

# {timestamp: int, sekcje: int, tryb: bool, ilosc: czas|litry}
class ProgramBlock:
    def __init__(self, start_czas_od_epoch: int, sekcja: int, tryb: bool, ilosc: float = 0):
        self.start_czas_od_epoch = start_czas_od_epoch
        self.sekcja = sekcja
        self.tryb = tryb
        self.ilosc = ilosc
        if tryb == tryb_podlewania_czasem:
            self.start_value = self.start_czas_od_epoch
        else:
            self.start_value = 0.0
        self.current_value = self.start_value

    def zmodyfikuj_ilosc(self, next_ilosc: float):
        self.ilosc = next_ilosc

    def add_delta(self, delta: float):
        self.current_value += delta

    def get_state(self):
        if self.current_value - self.start_value > self.ilosc:
            return False
        else:
            return True

    def __str__(self):
        return f"start: {self.start_czas_od_epoch} sekcja: {self.sekcja} tryb {self.tryb} ilosc: {self.ilosc}"

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

    def przelacz_tryb_podlewania(self) -> None:
        for i in self.ilosci_podlewania:
            if(self.tryb_podlewania == tryb_podlewania_czasem):
                i[1] = i[1] * config.avg_litry_na_minute;
            else:
                i[1] = i[1] / config.avg_litry_na_minute;
        self.tryb_podlewania = not self.tryb_podlewania;

    def czy_poprawny() -> bool:
        return False;


class plan_podlewania:
#---------------------------------POLA------------------------------------

    #           {nazwa_programu : program}
    programy : dict[str, program_podlewana] = {};
    # !!!!!! ZAKAZ MODYFIKOWANIA PÓL W PROGRAMACH PODLEWANIA TUTAJ !!!!!!!

    # W tym momencie wyobrażam sobie przygotowane bloczki z przyszłym podlewaniem na jakiś czas(jakoś 3 miesiące)
    # później będą one modyfikowane jednorazowo w kalendarzu w webapp
    # Zrobię, ale jeszcze nie teraz.

    programs_deletions: dict[(int, int), ProgramBlock] = {}
    free_blocks: list[ProgramBlock] = []

#---------------------------------POLA------------------------------------

    def __init__(self):
        pass

    def zmodyfikuj_program(self, nazwa_programu : str, nowy_program):
        # usuwa wszystkie małe(te robione w kalendarzu, jednorazowe) modyfikacje dla danego programu
        nowy_program.czy_poprawny();
        pass

    def change_ProgramBlock(self, timestamp: int, sekcja: int, block: ProgramBlock):
        self.programs_deletions[(timestamp, sekcja)] = block

    def dodaj_program(self): # Nie jestem pewnien czy dodać defaultowy program i potem go modyfikować czy podać jako argument nowy program
        pass

    def usun_program(self, nazwa_programu : str):
        self.programy.pop(nazwa_programu)

    def wyczysc_kolejke_do_wykonania(self):
        pass

    def add_free_block(self, block: ProgramBlock):
        self.free_blocks.append(block)

    def aktualne_stany_sekcji(self) -> dict:

        planowe_zmiany = {}

        # jezeli dzien tygodnia == true
        for program_name in self.programy.keys():

            if self.programy[program_name].w_ktore_dni_tygodnia_podlewac[czas_globalny.get_weekday()]:
                pass
        
        for block in self.free_blocks:
            planowe_zmiany[block.sekcja] = block.should_end()

        return planowe_zmiany


        # {sekvjaID: stan, } logika odnoscie aktualnego stanu (worker moze wlaczac przelaczniki za pomoca tego)

    def usun_stare_bloki(self, timestamp):
        pass

    def load_plan(self):
        pass # ladowanie planu z bazydanych (moze tymczasowo json)

# Block = {timestamp: int, sekcje: int, tryb: bool, ilosc: czas|litry}
# w plan dodac overwrite { (timestamp, sekcja): Block) }
# w plan dodac free_blocks: Block[]
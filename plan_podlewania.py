from konfiguracja import config

# coś do mierzenia czasu, godzina, nie wiem co dokładnie jeszcze
class czas:
    pass


# w c++ były by to constexpry
tryb_podlewania_czasem = True;
tryb_podlewania_iloscia = False;

class program_podlewana:
#---------------------------------POLA------------------------------------
    nazwa_programu : str; # aby było przyjemnie

    godzina_rozpoczecia : czas | None; # tak jak powyżej nie wiem co to będzie

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

        # brakuje defaultowej godziny
        self.godzina_rozpoczecia = None;

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

    def zmodyfikuj_ilosc(self, id_sekcji : int, nowa_ilosc = float):
        for i in range(0, len(self.ilosci_podlewania)):
            if(self.ilosci_podlewania[i][0] == id_sekcji):
                self.ilosci_podlewania[i][1] = nowa_ilosc;


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

#---------------------------------POLA------------------------------------

    def __init__(self):
        pass

    def zmodyfikuj_program(self, nazwa_programu : str, nowy_program):
        # usuwa wszystkie małe(te robione w kalendarzu, jednorazowe) modyfikacje dla danego programu
        nowy_program.czy_poprawny();
        pass

    def dodaj_program(self): # Nie jestem pewnien czy dodać defaultowy program i potem go modyfikować czy podać jako argument nowy program
        pass

    def usun_program(self, nazwa_programu : str):
        pass

    def wyczysc_kolejke_do_wykonania(self):
        pass







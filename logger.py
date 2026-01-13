from czas import czas_globalny
from konfiguracja import config

class Waznosc:
    INFO = 0;
    WARNING = 1;
    KRYTYCZNE = 2;
    HARDWARE = 3;

def waznosc_str(waznosc : int):
    if(waznosc == Waznosc.INFO):
        return "INFO";
    if(waznosc == Waznosc.WARNING):
        return "WARNING";
    if(waznosc == Waznosc.KRYTYCZNE):
        return "KRYTYCZNE";
    if(waznosc == Waznosc.HARDWARE):
        return "HARDWARE";
    assert(False);

def str_waznosc(waznosc : str):
    if(waznosc == "INFO"):
        return Waznosc.INFO;
    if(waznosc == "WARNING"):
        return Waznosc.WARNING;
    if(waznosc == "KRYTYCZNE"):
        return Waznosc.KRYTYCZNE;
    if(waznosc == "HARDWARE"):
        return Waznosc.HARDWARE;
    print(f"Nie znaleziono: {waznosc}");
    assert(False);

# co jakiś czas pewnie należy skasować plik loga
class Logger:
    sciezka_pliku : str;         

    def __init__(self, sciezka_pliku = config.plik_z_logiem):
        self.sciezka_pliku = sciezka_pliku;

    def log(self, wiadomosc, waznosc : int = Waznosc.INFO) -> None:
        # format wpisu to (czas) | (ważność) | (wiadomosc)\n
        # wiadomość ze znakami tylko w ascii
        with open(self.sciezka_pliku, 'a', encoding="ascii") as fd:
            do_zapisania = f"{czas_globalny.ladny_str()} | {waznosc_str(waznosc)} | {wiadomosc}\n";
            if(config.printuj_logi):
                print(do_zapisania, end = "");
            fd.write(do_zapisania);
    
    def przeczytaj_logi(self) -> tuple[str, str, str, str]:
        with open(self.sciezka_pliku, 'r', encoding="ascii") as fd:
            przeczytane = fd.readlines();
        
        info = [];
        warningi = [];
        krytyczne = [];
        hardware = [];
        for linia in przeczytane:
            podzielone = linia.split(" | ");
            waznosc = str_waznosc(podzielone[2]);
            
            # skladam z powrotem bez waznosci
            zlaczone_z_powrotem = f"{podzielone[0]} | {podzielone[1]} | {podzielone[3]}";

            if  (waznosc == Waznosc.INFO):
                info.append(zlaczone_z_powrotem);
            elif(waznosc == Waznosc.WARNING):
                warningi.append(zlaczone_z_powrotem);
            elif(waznosc == Waznosc.KRYTYCZNE):
                krytyczne.append(zlaczone_z_powrotem);
            elif(waznosc == Waznosc.HARDWARE):
                hardware.append(zlaczone_z_powrotem);
            else:
                assert(False);

        # index 0 to najnowszy log
        return info[::-1], warningi[::-1], krytyczne[::-1], hardware[::-1];

logger_globalny = Logger();

# testy

# logger_globalny.przygotuj_do_pisania();
# logger_globalny.log("test1");
# logger_globalny.log("test2", Waznosc.INFO);
# logger_globalny.log("test3", Waznosc.WARNING);
# logger_globalny.log("test4", Waznosc.KRYTYCZNE);
# print(logger_globalny.przeczytaj_logi());

# testy

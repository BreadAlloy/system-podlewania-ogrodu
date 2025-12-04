from czas import czas_globalny

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
    fd : int = 0;  # file descriptor
    sciezka_pliku : str;         

    def __init__(self, sciezka_pliku = "logi.txt"):
        self.sciezka_pliku = sciezka_pliku;

    def przygotuj_do_pisania(self):
        # wywołuje się tylko jeśli zamierza się pisać do pliku, przeczytać można bez tego
        assert(self.fd == 0); # został już przygotowany do pisania
        self.fd = open(self.sciezka_pliku, 'a', encoding="ascii"); # ascii, aby plik mniejszy był

    def log(self, wiadomosc, waznosc : int = Waznosc.INFO) -> None:
        # format wpisu to (czas) | (ważność) | (wiadomosc)\n
        # wiadomość ze znakami tylko w ascii
        assert(self.fd != 0); # plik nie przygotowany zapisu
        self.fd.write(f"{czas_globalny.ladny_str()} | {waznosc_str(waznosc)} | {wiadomosc}\n");
    
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

        return info, warningi, krytyczne, hardware;

    def __del__(self):
        if(self.fd != 0):
            self.fd.close();

logger_globalny = Logger();

# testy

# logger_globalny.przygotuj_do_pisania();
# logger_globalny.log("test1");
# logger_globalny.log("test2", Waznosc.INFO);
# logger_globalny.log("test3", Waznosc.WARNING);
# logger_globalny.log("test4", Waznosc.KRYTYCZNE);
# print(logger_globalny.przeczytaj_logi());

# testy

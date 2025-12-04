from .models import HistoriaZdarzen

class SterownikSekcji:
    def aktywuj_zawor(self, nr_zaworu, nr_sekcji):
        HistoriaZdarzen.loguj(
            typ='INFO', 
            wiadomosc=f"Rozpoczęto próbę aktywacji zaworu {nr_zaworu}.", 
            sekcja=nr_sekcji
        )

        try:
            self._wyslij_komende_aktywacji(nr_zaworu) 
            HistoriaZdarzen.loguj(
                typ='START', 
                wiadomosc=f"Zawór {nr_zaworu} został pomyślnie aktywowany.", 
                sekcja=nr_sekcji
            )
            return True

        except Exception as e:
            HistoriaZdarzen.loguj(
                typ='ERROR', 
                wiadomosc=f"KRYTYCZNY BŁĄD aktywacji zaworu {nr_zaworu}: {e}", 
                sekcja=nr_sekcji
            )
            return False

    def deaktywuj_zawor(self, nr_zaworu, nr_sekcji):
        HistoriaZdarzen.loguj(
            typ='INFO', 
            wiadomosc=f"Rozpoczęto próbę deaktywacji zaworu {nr_zaworu}.", 
            sekcja=nr_sekcji
        )

        try:
            self._wyslij_komende_deaktywacji(nr_zaworu)
            HistoriaZdarzen.loguj(
                typ='STOP', 
                wiadomosc=f"Zawór {nr_zaworu} został pomyślnie deaktywowany (zamknięty).", 
                sekcja=nr_sekcji
            )
            return True

        except Exception as e:
            HistoriaZdarzen.loguj(
                typ='ERROR', 
                wiadomosc=f"KRYTYCZNY BŁĄD deaktywacji zaworu {nr_zaworu}: {e}", 
                sekcja=nr_sekcji
            )
            return False

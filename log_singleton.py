from django.utils import timezone
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(name)

class WpisLogu:
    TYP_CHOICES = {
        'INFO': 'Informacja',
        'START': 'Włączenie',
        'STOP': 'Wyłączenie',
        'ERROR': 'Błąd',
    }

    def init(self, typ: str, wiadomosc: str, nr_sekcji: Optional[int] = None):
        self.data = timezone.now()
        self.typ = typ
        self.wiadomosc = wiadomosc
        self.nr_sekcji = nr_sekcji

    def str(self):
        return f"[{self.data.strftime('%Y-%m-%d %H:%M')}] {self.typ}: {self.wiadomosc}"

  class HistoriaZdarzenSingleton:
    _instance = None #  zmienna do przechowywania instancji

    historia: List[WpisLogu] = [] 

    def new(cls):
        """
        Zapewnia, że tworzona jest tylko jedna instancja klasy.
        """
        if cls._instance is None:
            cls._instance = super(HistoriaZdarzenSingleton, cls).new(cls)
            # Inicjalizacja może się odbywać tutaj, jeśli potrzebna
        return cls._instance

    def loguj(self, typ: str, wiadomosc: str, sekcja: Optional[int] = None):
        """
        Dodaje nowy wpis logu do listy w pamięci.
        """
        try:
            nowy_wpis = WpisLogu(typ, wiadomosc, sekcja)
            self.historia.insert(0, nowy_wpis)
            logger.info(f"Zalogowano w Singletonie: {nowy_wpis}")

Opcjonalnie: Ograniczenie wielkości listy, żeby nie zapchać pamięci
if len(self.historia) > 1000:
self.historia.pop() 
        except Exception as e:
            logger.error(f"Błąd zapisu do Singletonu: {e}")

    def pobierz_historie(self) -> List[WpisLogu]:
        """
        Zwraca całą listę zdarzeń (najnowsze na początku).
        """
        return self.historia

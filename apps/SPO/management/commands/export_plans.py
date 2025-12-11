import json
import os
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.SPO.logger import SystemLogger

# Dodajemy ścieżkę główną projektu, aby Python widział pliki z roota
sys.path.append(str(settings.BASE_DIR))

class Command(BaseCommand):
    help = 'Eksportuje obiekty planów z pliku przykladowe_programy_podlewania.py do JSON'

    def handle(self, *args, **options):
        logger = SystemLogger()
        
        try:
            from przykladowe_programy_podlewania import p1, p2, p3, p4, p5
            # Tworzymy listę ręcznie, bo w tamtym pliku są to luźne zmienne
            lista_programow = [p1, p2, p3, p4, p5]
        except ImportError as e:
            msg = f"Błąd importu: {e}. Upewnij się, że plik 'przykladowe_programy_podlewania.py' jest w głównym folderze."
            self.stdout.write(self.style.ERROR(msg))
            return

        data_to_export = []

        self.stdout.write(f"Znaleziono {len(lista_programow)} przykładowych programów. Przetwarzanie...")

        for program in lista_programow:
            try:
                tryb_str = "CZAS (min)" if program.tryb_podlewania else "ILOŚĆ (litry)"

                program_dict = {
                    'nazwa': program.nazwa_programu,
                    # rzutujemy zegarek na str, bo JSON nie ogarnia obiektów
                    'godzina_start': str(program.godzina_rozpoczecia), 
                    'tryb': tryb_str,
                    'co_ile_dni': program.co_ile_dni_podlac,
                    'dni_tygodnia': {
                        'Pon': program.w_ktore_dni_tygodnia_podlewac[0],
                        'Wt': program.w_ktore_dni_tygodnia_podlewac[1],
                        'Sr': program.w_ktore_dni_tygodnia_podlewac[2],
                        'Czw': program.w_ktore_dni_tygodnia_podlewac[3],
                        'Pt': program.w_ktore_dni_tygodnia_podlewac[4],
                        'Sob': program.w_ktore_dni_tygodnia_podlewac[5],
                        'Nd': program.w_ktore_dni_tygodnia_podlewac[6],
                    },
                    'sekcje': []
                }

                for sekcja in program.ilosci_podlewania:
                    # sekcja to lista [id, ilosc]
                    id_sekcji = sekcja[0]
                    ilosc = sekcja[1]
                    
                    if ilosc > 0:
                        program_dict['sekcje'].append({
                            'id_sekcji': id_sekcji,
                            'ilosc': ilosc
                        })

                data_to_export.append(program_dict)
            
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Błąd przy przetwarzaniu programu '{program.nazwa_programu}': {e}"))

        # 3. Zapis do pliku
        filename = os.path.join(settings.BASE_DIR, "plany_export.json")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_export, f, indent=4, ensure_ascii=False)
            
            msg = f"Sukces! Wyeksportowano {len(data_to_export)} programów do: {filename}"
            self.stdout.write(self.style.SUCCESS(msg))
            logger.log(f"Wykonano eksport planów do JSON.")
            
        except Exception as e:
            msg = f"Błąd zapisu pliku: {e}"
            self.stdout.write(self.style.ERROR(msg))
            logger.log(msg)

import os
from datetime import datetime
import sys

class SystemLogger:
    _instance = None
    # Plik logów będzie w głównym katalogu projektu
    LOG_FILE = "system_logs.txt"

    def __new__(cls):
        # Implementacja wzorca Singleton - tylko jedna instancja klasy może istnieć
        if cls._instance is None:
            cls._instance = super(SystemLogger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        """
        Zapisuje wiadomość w formacie: czas | wiadomość
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{now} | {message}"

        # 1. Zapis do pliku (żeby pokazać na stronie WWW)
        try:
            with open(self.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(formatted_message + "\n")
        except Exception as e:
            print(f"Błąd zapisu loga do pliku: {e}")

        print(formatted_message, file=sys.stdout)

    def get_logs(self, limit=50):
        """
        Pobiera ostatnie X linii z pliku logów do wyświetlenia na stronie
        """
        if not os.path.exists(self.LOG_FILE):
            return []
        
        with open(self.LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        return lines[-limit:][::-1]
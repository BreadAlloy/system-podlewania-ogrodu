import logging

Odwołanie do skonfigurowanego loggera
prosty_logger = logging.getLogger('ProstyLogger')

def loguj_prosty_wpis(wiadomosc: str):
    """
    Zapisuje prosty wpis logu w formacie "czas | wiadomość" do pliku.
    """
    prosty_logger.info(wiadomosc)

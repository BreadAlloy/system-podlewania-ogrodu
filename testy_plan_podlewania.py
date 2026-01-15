import unittest
from datetime import datetime
from plan_podlewania import program_podlewania, plan_podlewania, tryb_podlewania_czasem, ProgramBlock

class MockWodomierz:
    def __init__(self):
        self.wartosc = 0
    def stan_wodomierza(self, obj):
        return self.wartosc

class TestSystemuPodlewania(unittest.TestCase):

    def setUp(self):

        self.plan = plan_podlewania()
        self.wodomierz = MockWodomierz()

    def test_dodawanie_programu(self):

        prog = program_podlewania()
        prog.nazwa_programu = "Testowy"
        prog.co_ile_dni_podlac = 1

        prog.zmodyfikuj_ilosc(1, 10.0)
        prog.zmodyfikuj_ilosc(2, 5.0)
        
        self.plan.dodaj_program(prog)
        
        self.assertEqual(len(self.plan.przyszle_ProgramBloki), 2)
        self.assertEqual(self.plan.programy["Testowy"].nazwa_programu, "Testowy")

    def test_przelaczanie_trybow(self):

        prog = program_podlewania()
        prog.tryb_podlewania = tryb_podlewania_czasem
        prog.zmodyfikuj_ilosc(1, 10.0)
        
    def test_logika_update_zakonczenie_blokow(self):

        prog = program_podlewania()
        prog.zmodyfikuj_ilosc(1, 1.0)
        self.plan.dodaj_program(prog)

        blok = self.plan.przyszle_ProgramBloki[0]
        self.plan.wykonywane_ProgramBloki.append(ProgramBlock(blok.czas_wykonania.czas_od_epoch, 1, True, prog, 60))
        
        self.plan.last_check_time -= 30 
        aktywna_sekcja = self.plan.update(self.wodomierz)
        self.assertEqual(aktywna_sekcja, 1, "Sekcja powinna być wciąż aktywna")
        
        self.plan.last_check_time -= 40
        aktywna_sekcja = self.plan.update(self.wodomierz)
        self.assertIsNone(aktywna_sekcja, "Sekcja powinna się wyłączyć po przekroczeniu czasu")

    def test_generowanie_kolejnego_terminu(self):

        prog = program_podlewania()
        prog.co_ile_dni_podlac = 1
        self.plan.dodaj_program(prog)
        
        pierwszy_termin = self.plan.przyszle_ProgramBloki[0].czas_wykonania.czas_od_epoch
        
        nowy_blok = self.plan.przyszle_ProgramBloki[0].wygeneruj_kolejny()
        
        roznica = nowy_blok.czas_wykonania.czas_od_epoch - pierwszy_termin
        self.assertGreaterEqual(roznica, 86400)

if __name__ == '__main__':
    unittest.main()

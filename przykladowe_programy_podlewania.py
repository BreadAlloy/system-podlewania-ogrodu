from plan_podlewania import program_podlewana, tryb_podlewania_czasem, tryb_podlewania_iloscia, plan_podlewania
from czas import zegarek

def przykladowy_program_podlewania_1() -> program_podlewana:
    program = program_podlewana();
    program.nazwa_programu = "Podlewanie trawy";
    program.godzina_rozpoczecia = zegarek(2, 00); #2:00
    program.tryb_podlewania = tryb_podlewania_czasem;
    program.w_ktore_dni_tygodnia_podlewac = [True, True, True, True, True, False, True];
    program.zmodyfikuj_ilosc(3, 15.0);
    program.zmodyfikuj_ilosc(4, 15.0);
    program.zmodyfikuj_ilosc(5, 15.0);
    program.zmodyfikuj_ilosc(6, 15.0);
    program.zmodyfikuj_ilosc(7, 15.0);
    program.zmodyfikuj_ilosc(8, 15.0);
    program.zmodyfikuj_ilosc(9, 15.0);
    program.co_ile_dni_podlac = 2;
    return program;

def przykladowy_program_podlewania_2() -> program_podlewana:
    program = program_podlewana();
    program.nazwa_programu = "Podlewanie nowych drzew";
    program.godzina_rozpoczecia = zegarek(00, 00); # 24:00
    program.tryb_podlewania = tryb_podlewania_czasem;
    program.w_ktore_dni_tygodnia_podlewac = [True, True, True, True, True, True, True];
    program.zmodyfikuj_ilosc(0, 90.0);
    program.co_ile_dni_podlac = 1;
    return program;

def przykladowy_program_podlewania_3() -> program_podlewana:
    program = program_podlewana();
    program.nazwa_programu = "Podlewanie rabatek wieczorem";
    program.godzina_rozpoczecia = zegarek(21, 00); # 21:00
    program.tryb_podlewania = tryb_podlewania_iloscia;
    program.w_ktore_dni_tygodnia_podlewac = [True, True, True, True, True, True, True];
    program.zmodyfikuj_ilosc(1, 400.0);
    program.zmodyfikuj_ilosc(2, 500.0);
    program.co_ile_dni_podlac = 1;
    return program;

def przykladowy_program_podlewania_4() -> program_podlewana:
    program = program_podlewana();
    program.nazwa_programu = "Podlewanie rabatek nad ranem";
    program.godzina_rozpoczecia = zegarek(5, 00); # 5:00
    program.tryb_podlewania = tryb_podlewania_iloscia;
    program.w_ktore_dni_tygodnia_podlewac = [True, True, True, True, True, True, True];
    program.zmodyfikuj_ilosc(1, 500.0);
    program.zmodyfikuj_ilosc(2, 400.0);
    program.co_ile_dni_podlac = 1;
    return program;

def przykladowy_program_podlewania_5() -> program_podlewana:
    program = program_podlewana();
    program.nazwa_programu = "Podlewanie dodatkowe";
    program.godzina_rozpoczecia = zegarek(12, 00); # 12:00
    program.tryb_podlewania = tryb_podlewania_czasem;
    program.w_ktore_dni_tygodnia_podlewac = [True, False, True, False, True, False, True];
    program.zmodyfikuj_ilosc(10, 5.0);
    program.zmodyfikuj_ilosc(11, 15.0);
    program.zmodyfikuj_ilosc(12, 45.0);
    program.zmodyfikuj_ilosc(13, 20.0);
    program.zmodyfikuj_ilosc(14, 1.0);
    program.co_ile_dni_podlac = 3;
    return program;

# TESTY

# p1 = przykladowy_program_podlewania_1();
# p2 = przykladowy_program_podlewania_2();
# p3 = przykladowy_program_podlewania_3();
# p4 = przykladowy_program_podlewania_4();
# p5 = przykladowy_program_podlewania_5();
# print(p1);
# print(p2);
# print(p3);
# print(p4);
# print(p5);
# print("="*70);
# p5.przelacz_tryb_podlewania()
# print(p5);
# p5.przelacz_tryb_podlewania()
# print(p5);

# plan = plan_podlewania();
# plan.dodaj_program(p1.nazwa_programu, p1);
# plan.dodaj_program(p2.nazwa_programu, p2);
# plan.dodaj_program(p3.nazwa_programu, p3);
# plan.dodaj_program(p4.nazwa_programu, p4);
# plan.dodaj_program(p5.nazwa_programu, p5);

# # print(plan.przyszle_ProgramBloki);
# # print(plan.przyszle_ProgramBloki[0]);
# temp = plan.przyszle_ProgramBloki.copy();
# import heapq
# while(len(temp) > 0):
#     print(heapq.heappop(temp));

# import time
# while(True):
#     time.sleep(1.0);
#     plan.update();

#TESTY
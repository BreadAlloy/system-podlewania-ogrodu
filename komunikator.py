from multiprocessing.connection import Listener, Client

class kody_komunikatow:
    # namespace do wsadzania kodow komunikatow po których potem będzie można ifować
    ROZLACZ = 0;
    USUN_PROGRAM = 1;
    ZMODYFIKUJ_PROGRAM = 2;

client_polaczenia = True;
serwer_polaczenia = False;

class komunikator:
    port : int
    # connection
    flaga : bool

    def __init__(self, port):
        self.port = port;
        self.connection = None;
        self.flaga = None;

    def serwuj(self):
        assert(self.flaga == None);
        self.flaga = serwer_polaczenia;
        address = ('localhost', self.port);
        self.listener = Listener(address);

    def polacz(self):
        assert(self.connection == None);
        if(self.flaga == serwer_polaczenia):
            self.connection = self.listener.accept();
            return;
        assert(self.flaga == None);
        self.flaga = client_polaczenia;
        address = ('localhost', self.port);
        self.connection = Client(address);

    def wyslij(self, kod_komunikatu : int, wiadomosc : any):
        assert(self.connection != None);
        wysylane = (kod_komunikatu, wiadomosc);
        self.connection.send(wysylane);

    def odbierz(self) -> tuple[int, any]:
        assert(self.connection != None);
        otrzymane = self.connection.recv();
        if(otrzymane[0] == kody_komunikatow.ROZLACZ):
            self.rozlacz();
        return otrzymane;

    def rozlacz(self):
        assert(self.connection != None);
        self.wyslij(kody_komunikatow.ROZLACZ, "close");
        self.connection.close();
        self.connection = None;

    def __del__(self):
        if(self.connection != None):
            self.rozlacz();


# ---=== TESTY ===---
# class tester():
#     ldld = 2222;
#     dddas = ["asda", 111];
#     terst = True;

#     def __str__(self):
#         return f"{self.ldld}, {self.dddas}, {self.terst}"

#     def __repr__(self):
#         return self.__str__();

# test1 = komunikator(9292);
# test2 = komunikator(9292);

# test1.serwuj();

# test2.polacz();

# test1.polacz();

# cos = tester();

# test1.wyslij(kody_komunikatow.USUN_PROGRAM, cos);
# print(test2.odbierz());

# test2.wyslij(kody_komunikatow.USUN_PROGRAM, cos);
# print(test1.odbierz());

# test1.rozlacz();
# print(test2.odbierz());

# ---=== TESTY ===---

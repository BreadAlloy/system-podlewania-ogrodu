from multiprocessing.connection import Listener, Client

class kody_komunikatow:
    # namespace do wsadzania kodow komunikatow po których potem będzie można ifować
    ROZLACZ = 0;
    USUN_PROGRAM = 1;
    ZMODYFIKUJ_PROGRAM = 2;
    DODAJ_PROGRAM = 3;

kod_komunikatu_str = {
    0 : "kod: ROZLACZ",
    1 : "kod: USUN_PROGRAM",
    2 : "kod: ZMODYFIKUJ_PROGRAM",
    3 : "kod: DODAJ_PROGRAM",
};

class kod_komunikatu:
    def __init__(self, kod : int):
        self.kod = kod;

    def __str__(self) -> str:
        return kod_komunikatu_str[self.kod];

    def __repr__(self) -> str:
        return self.__str__();

client_polaczenia = True;
serwer_polaczenia = False;

class komunikator:
    # port : int
    # # connection
    # flaga : bool
    # ip : str

    def __init__(self, ip, port):
        self.port = port;
        self.ip = ip;
        self.connection = None;
        self.flaga = None;

    def serwuj(self):
        assert(self.flaga == None);
        assert(self.connection == None);
        self.flaga = serwer_polaczenia;
        self.address = (self.ip, self.port);
        with Listener(self.address, authkey=b'nic') as listener:
            self.connection = listener.accept();
            print('connection accepted from', listener.last_accepted);

    def polacz(self):
        assert(self.connection == None);
        assert(self.flaga == None);
        self.flaga = client_polaczenia;
        self.address = (self.ip, self.port);
        self.connection = Client(self.address, authkey=b'nic');

    def wyslij(self, kod : int, wiadomosc : any):
        assert(self.connection != None);
        wysylane = (kod_komunikatu(kod), wiadomosc);
        self.connection.send(wysylane);

    def odbierz(self) -> tuple[kod_komunikatu, any] | None:
        assert(self.connection != None);
        if(not self.connection.poll()):
            return None; # Nie ma nic do odebrania
        otrzymane = self.connection.recv();
        if(otrzymane[0].kod == kody_komunikatow.ROZLACZ):
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

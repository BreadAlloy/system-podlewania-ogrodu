from komunikator import *
from konfiguracja import *




from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'

with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        print('connection accepted from', listener.last_accepted)

        conn.send([2.25, None, 'junk', float])

        conn.send_bytes(b'hello')

        conn.send_bytes(array('i', [42, 1729]))



class tester():
    ldld = 2222;
    dddas = ["asda", 111];
    terst = True;

    def __str__(self):
        return f"{self.ldld}, {self.dddas}, {self.terst}"

    def __repr__(self):
        return self.__str__();

test1 = komunikator(config.port_do_komunikacji);

test1.serwuj();

# test1.polacz();

print("Polaczono")

cos = tester();

test1.wyslij(kody_komunikatow.USUN_PROGRAM, cos);

print(test1.odbierz());

test1.rozlacz();

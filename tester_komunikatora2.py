from komunikator import *
from konfiguracja import *

from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait

from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)

with Client(address, authkey=b'secret password') as conn:
    print(conn.recv())                  # => [2.25, None, 'junk', float]

    print(conn.recv_bytes())            # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr))    # => 8
    print(arr)                          # => array('i', [42, 1729, 0, 0, 0])

class tester():
    ldld = 2222;
    dddas = ["asda", 111];
    terst = True;

    def __str__(self):
        return f"{self.ldld}, {self.dddas}, {self.terst}"

    def __repr__(self):
        return self.__str__();

test2 = komunikator(config.port_do_komunikacji);

test2.polacz();

cos = tester();

print(test2.odbierz());

test2.wyslij(kody_komunikatow.USUN_PROGRAM, cos);

print(test2.odbierz());
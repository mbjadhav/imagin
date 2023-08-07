#import sht85
import time
import datetime
import math
import serial
import socket

from sht85 import SHT85
from interlock.Interlock import Interlock
from relayboard.RelayBoard import RelayBoard



s = socket.socket()
TCP_IP = '192.168.0.216'
TCP_PORT = 12400
BUFFER_SIZE = 1024
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    c,addr = s.accept()
    tmodule = Interlock.read_tempmodule()

    outdata = f"{tmodule}\n"
    print(outdata)
    c.send(''.join(outdata).encode('utf-8'))




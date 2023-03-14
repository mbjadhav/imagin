#import sht85
import time
import math
import serial
import socket

from sht85 import SHT85
from interlock.Interlock import Interlock
from relayboard.RelayBoard import RelayBoard
mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)
'''
TCP_IP = '192.168.0.218'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)
'''
fname_IntState = time.strftime("InterlockStatusData_%Y%m%d%H%M%S.txt")
fInterlock=open(fname_IntState, "a+")
fInterlock.write(f"EventTime\taTemp\tRH\tDP\tcTemp\tmTemp\tsLid\tsVacuu\tsPressure\n")
fInterlock.close()
print(f"EventTime\taTemp\tRH\tDP\tcTemp\tmTemp\tsLid\tsVacuu\tsPressure\n")

SHT85.periodic(mps,rep)
#Interlock.check_interlock()
#RelayBoard.relwr(5, 1)

Interlock.set_gled(1)

time.sleep(1)
try:
    while True:
        t,rh, dp = Interlock.read_sht85value()
        tchuck = Interlock.read_tempchuck()
        #tmodule = Interlock.read_tempmodule()
        tmodule=0
        slid, svacuum, spressure = Interlock.read_switches()
        tevent = time.strftime("%Y%m%d%H%M%S")

        print(f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\n")
        fInterlock=open(fname_IntState, "a+")
        fInterlock.write(f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\n")
        fInterlock.close()
        time.sleep(1)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    SHT85.stop()

Interlock.reset_alarms()

SHT85.stop()

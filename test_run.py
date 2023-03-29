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

s = socket.socket()
TCP_IP = '192.168.0.218'
TCP_PORT = 12399
BUFFER_SIZE = 1024
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
c,addr = s.accept()

Interlock.reset_alarms()

fname_IntState = time.strftime("interlock_data/InterlockStatusData_%Y%m%d%H%M%S.txt")
fInterlock=open(fname_IntState, "a+")
fInterlock.write(f"EventTime\taTemp\tRH\tDP\tcTemp\tmTemp\tsLid\tsVacuu\tsPressure\tIsOkay\n")
fInterlock.close()
print(f"EventTime\taTemp\tRH\tDP\tcTemp\tmTemp\tsLid\tsVacuu\tsPressure\tIsOkay\n")

SHT85.periodic(mps,rep)
#Interlock.check_interlock()
#RelayBoard.relwr(5, 1)

IsOkay = 1
count_stable = 0
count_fails = 0
afterfail_stable = 0
#Interlock.set_gled()
time.sleep(1)
try:
    while True:
        t,rh, dp = Interlock.read_sht85value()
        tchuck = Interlock.read_tempchuck()
        tmodule = Interlock.read_tempmodule()
        #tmodule=0
        slid, svacuum, spressure = Interlock.read_switches()
        tevent = time.strftime("%Y%m%d%H%M%S")

        if slid == 1 and svacuum == 1 and spressure == 1 and abs(tchuck - 15)<10 and abs(rh-0)<0.5 and abs(tmodule-20)<10 and IsOkay:
            Interlock.set_gled()
            count_stable += 1
            if count_fails > 0:
                count_fails = 0
            if count_fails > 10:
                Interlock.set_yled()
        elif count_stable>10:
            Interlock.switch_peltier(1)
            Interlock.power_peltier()
            Interlock.enable_lv()
            Interlock.enable_hv()
            if slid == 0 or svacuum == 0 or spressure == 0 or abs(tchuck - 15)>10 or abs(rh-0)>0.5 or abs(tmodule-20)>10:
                count_fails += 1
                if count_fails < 6:
                    Interlock.set_yled()
                    Interlock.set_gled(1)
                elif count_fails > 5:
                    Interlock.set_yled(1)
                    Interlock.set_gled(1)
                    Interlock.set_rled()
                    if count_fails < 21 or count_fails%60 == 0: Interlock.set_alarm()
                    else: Interlock.set_alarm(1)
                    Interlock.enable_hv(1)
                    Interlock.enable_lv(1)
                    Interlock.power_peltier(0)
                    IsOkay = 0
            elif IsOkay:
                count_fails = 0
                Interlock.set_gled()
                Interlock.set_yled(1)
                Interlock.set_rled(1)
                Interlock.set_alarm(1)
            else:
                Interlock.set_yled()
                if Interlock.get_rled() == 0:
                    afterfail_stable += 1
                    if afterfail_stable%60 == 0: Interlock.set_alarm()
                    else: Interlock.set_alarm(1)               
        else:
            Interlock.set_yled()
            Interlock.set_gled(1)

        outdata = f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\t{IsOkay}\n"
        #outdata = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(tevent, t, rh, dp, tchuck, tmodule, slid, svacuum, spressure, IsOkay)
        print(outdata)
        c.send(''.join(outdata).encode('utf-8'))
        #c.close()

        fInterlock=open(fname_IntState, "a+")
        fInterlock.write(f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\t{IsOkay}\n")
        fInterlock.close()
        time.sleep(1)
    #c.close()
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    SHT85.stop()

Interlock.reset_alarms()

#SHT85.stop()

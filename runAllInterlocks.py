#import sht85
import time
import datetime
import math
import serial
import socket

from sht85 import SHT85
from interlock.Interlock import Interlock
from relayboard.RelayBoard import RelayBoard
mps = 2 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)

s = socket.socket()
TCP_IP = '192.168.0.216'
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
#SHT85.single_shot(rep)
#Interlock.check_interlock()
#RelayBoard.relwr(5, 1)

IsOkay = 0 # initialized with 0
count_stable = 0
count_fails = 0
afterfail_stable = 0
switchon_ps_once = 0
#Interlock.set_gled()
time.sleep(1)
try:
    while True:
        t,rh, dp = Interlock.read_sht85value()
        tchuck = Interlock.read_tempchuck()
        tmodule = Interlock.read_tempmodule()
        slid, svacuum, spressure = Interlock.read_switches()
        tevent = datetime.datetime.now().strftime("%y/%m/%d-%H:%M:%S") 
        #Interlock.powerON_peltier()
        #Interlock.enable_lv() # DY - bypass for source scan

        # IsOkay will store 1 only if truly all condition are satisfied
        if slid == 1 and svacuum == 1 and spressure == 1 and abs(tchuck)<60 and abs(rh-0)<2 and tmodule<45:
            IsOkay=1
            
        if slid == 1 and svacuum == 1 and spressure == 1 and abs(tchuck)<60 and abs(rh-0)<2 and tmodule<45 and IsOkay:
            Interlock.set_gled()
            count_stable += 1
            if count_fails > 0:
                count_fails = 0
            if count_fails > 10:
                Interlock.set_yled()
            if switchon_ps_once == 0 and count_stable > 20: # Now, we are ready to turn on the all instruments
                Interlock.switch_peltier(1)   # 0 for heating (default) and 1 for cooling 
                Interlock.powerON_peltier()
                Interlock.enable_lv()
                Interlock.enable_hv()
                switchon_ps_once = 1
            #if count_stable == 200:
                #Interlock.switch_peltier()

        elif count_stable>20:
            if slid == 0 or svacuum == 0 or spressure == 0 or abs(tchuck)>60 or abs(rh-0)>2 or tmodule>45:
                interlockTriggerThreshold = 2
                count_fails += 1
                if count_fails <= interlockTriggerThreshold: # if IsOkay condition fails one or two times in series
                    Interlock.set_yled() # just yellow
                    Interlock.set_gled(1)
                elif count_fails > interlockTriggerThreshold: # if IsOkay condition fails more then two times in series
                    Interlock.set_yled(1)
                    Interlock.set_gled(1)
                    Interlock.set_rled() # interlock triggered - red LED 
                    if count_fails < 21 or count_fails%60 == 0: Interlock.set_alarm()
                    else: Interlock.set_alarm(1)
                    if count_fails == (interlockTriggerThreshold+1): # interlock triggered - shut down all
                        Interlock.disable_hv()
                        Interlock.disable_lv()
                        Interlock.powerOFF_peltier()
                        IsOkay = 0
            elif IsOkay:
                count_fails = 0
                Interlock.set_gled()
                Interlock.set_yled(1)
                Interlock.set_rled(1)
                Interlock.set_alarm(1)
                # ??? 
                if tmodule > 35 or tchuck -5 < dp: 
                    if count_stable%10 == 0 : Interlock.set_yled()
                    else: Interlock.set_yled(1)
                # ???
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
        print(outdata)
        c.send(''.join(outdata).encode('utf-8'))
        #c.close()

        fInterlock=open(fname_IntState, "a+")
        fInterlock.write(f"{tevent}\t{t}\t{rh}\t{dp}\t{tchuck}\t{tmodule}\t{slid}\t{svacuum}\t{spressure}\t{IsOkay}\n")
        fInterlock.close()
        time.sleep(0.9)
    #c.close()
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    SHT85.stop()

Interlock.reset_alarms()

#SHT85.stop()

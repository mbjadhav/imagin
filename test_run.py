import sht85
import time
import math

from sht85 import SHT85
from interlock.Interlock import Interlock
from relayboard.RelayBoard import RelayBoard
mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)

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

        print('Time =', time.strftime("%Y%m%d%H%M%S"))
        print ('Temperature =', t)
        print ('Relative Humidity =', rh)
        print ('Dew Point =', dp)
        print ('Chuck Temperature =', tchuck)
        print ('Module Temperature =', tmodule)
        print ('Lid Switch =', slid)
        print ('Vacuum switch =', svacuum)
        print ('Pressure Switch =', spressure)
        time.sleep(1)

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    SHT85.stop()

Interlock.reset_alarms()

SHT85.stop()

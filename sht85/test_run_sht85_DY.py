import sht85
import time
import math

from sht85 import *
mps = 1 # accepted intervals 0.5, 1, 2, 4, 10 seconds
rep = 'HIGH' # Repeatability: HIGH, MEDIUM, LOW

filename = time.strftime("RaspberryPi_%Y%m%d%H%M%S.txt")
tmp_file=open(filename, "a+")
tmp_file.close()


#print ('serial number = ', sht85.sn())
time.sleep(0.5e-3)

sht85.periodic(mps,rep)
time.sleep(1)
try:
    while True:
        t,rh = sht85.read_data()
        dp = sht85.dew_point(t,rh)
        print('Time =', time.strftime("%Y%m%d%H%M%S"))
        print ('Temperature =', t)
        print ('Relative Humidity =', rh)
        print ('Dew Point =', dp)
        tmp_file=open(filename, "a+")
        tmp_file.write("%s %s %s %s\n"%(time.strftime("%Y%m%d%H%M%S"), t, rh, dp))
        tmp_file.close()
        time.sleep(mps)
        
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Killing Thread...")
    time.sleep(0.5e-3)
    sht85.stop()

sht85.stop()
